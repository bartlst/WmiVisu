import wmi
import winrm
from concurrent.futures import ThreadPoolExecutor
import time
import pythoncom
from website.models import *
from datetime import datetime
from sqlalchemy import func
from requests.exceptions import ReadTimeout


def convert_cim_date(cim_date_str):
    year = int(cim_date_str[:4])
    month = int(cim_date_str[4:6])
    day = int(cim_date_str[6:8])
    hour = int(cim_date_str[8:10])
    minute = int(cim_date_str[10:12])
    second = int(cim_date_str[12:14])

    dt = datetime(year, month, day, hour, minute, second)

    return dt


def ps_out_to_dict(output):
    """
    Parses the PowerShell output string into a list of dictionaries,
    considering '|&' as the end marker of each value.

    :param output: str - The PowerShell output as a string.
    :return: list - A list of dictionaries with parsed data.
    """
    # Split the output into lines and remove empty lines
    lines = [line.strip() for line in output.split('\n') if line.strip() and not line.startswith('-')]
    # Extract the header names
    headers = lines[0].split('|&')
    headers = [header.strip() for header in headers if header.strip()]

    # Create a list to store the parsed dictionaries
    parsed_data = []

    # Process the data lines
    for line in lines[1:]:
        # Split the line into values based on '|&' and strip whitespace
        values = line.split('|&')
        values = [value.strip() for value in values if value.strip()]

        # Map the values to the headers in a dictionary and add to the list
        if len(values) == len(headers):
            data_dict = dict(zip(headers, values))
            parsed_data.append(data_dict)

    return parsed_data


def ps_winrm_exec(file_name, session):
    with open(file_name) as script_file:
        script = script_file.read()
        response = session.run_ps(script)

        return response


USERNAME = 'admin'
PASSWORD = 'admin'
app = None
db = None


def wmi_check(host):
    with app.app_context():  # Utworzenie kontekstu aplikacji
        append_to_db = []
        session = winrm.Session(f'http://{host.hostname}:5985/wsman',
                                auth=('admin', 'admin'),
                                server_cert_validation='ignore',
                                transport='ntlm')
        session.protocol.read_timeout_sec = 45
        session.protocol.operation_timeout_sec = 45
        try:
            session.run_cmd('hostname')
        except winrm.exceptions.InvalidCredentialsError as e:
            host.connection_status = 2
        except Exception as e:
            host.connection_status = 0

        else:
            host.connection_status = 1
            try:
                os_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/os_info.ps1', session=session)
                motherboard_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/motherboard_info.ps1', session=session)
                gpu_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/gpu_info.ps1', session=session)
                cpu_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/cpu_info.ps1', session=session)
                ram_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/ram_info.ps1', session=session)
                services_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/services.ps1', session=session)
                disks_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/disk_measurements.ps1', session=session)
                crm_ps1_response = ps_winrm_exec(file_name='./application/ps_scripts/cpu_ram_measurements.ps1', session=session)
            except Exception as e:
                return None
            else:
                # # Services
                services = ps_out_to_dict(services_ps1_response.std_out.decode())
                # print(services)
                host_services = Spec_Service.query.filter_by(server_id=host.id).all()
                host_services_dict = {service.name: service for service in host_services}
                for service in services:
                    if not service['Name'] in host_services_dict:
                        new_service = Spec_Service(
                            server_id=host.id,
                            name=service['Name'],
                            watched=0
                        )
                        append_to_db.append(new_service)
                    else:
                        check_service = host_services_dict[service['Name']]
                        last_status = Info_Service.query.filter_by(service_id=check_service.id)\
                            .order_by(Info_Service.status_change_date.desc()).first()

                        if not last_status or last_status.status != service['Status']:
                            new_status = Info_Service(
                                service_id=check_service.id,
                                status=service['Status'],
                                status_change_date=datetime.now()
                            )
                            append_to_db.append(new_status)
                            # Add service status report
                # # DISK
                disks_measurement = ps_out_to_dict(disks_ps1_response.std_out.decode())
                # print(disks_measurement)
                # add measurement
                for disk in disks_measurement:
                    append_to_db.append(Info_DiskMeasurements(
                                server_id=host.id,
                                disk_id=disk['DiskID'],
                                measurement_date=datetime.now(),
                                total_space=disk['TotalSizeB'],
                                used_space=disk['UsedSpaceB'],
                                free_space=disk['FreeSpaceB']
                            ))

                # Specification
                os = ps_out_to_dict(os_ps1_response.std_out.decode())
                motherboard = ps_out_to_dict(motherboard_ps1_response.std_out.decode())
                gpu = ps_out_to_dict(gpu_ps1_response.std_out.decode())
                cpu = ps_out_to_dict(cpu_ps1_response.std_out.decode())
                ram = ps_out_to_dict(ram_ps1_response.std_out.decode())

                specification = Specification(
                    server_id=host.id,
                    os=str(os),
                    motherboard=str(motherboard),
                    cpu=str(cpu),
                    ram=str(ram),
                    gpu=str(gpu),
                    disk=str([{"ID": disk['DiskID'], 'Size': disk['TotalSizeB']} for disk in disks_measurement]),
                )
                if len(host.specification) == 0:
                    append_to_db.append(specification)
                elif (str(host.specification[-1].os) != specification.os or
                      str(host.specification[-1].motherboard) != specification.motherboard or
                      str(host.specification[-1].cpu) != specification.cpu or
                      str(host.specification[-1].ram) != specification.ram or
                      str(host.specification[-1].gpu) != specification.gpu or
                      str(host.specification[-1].disk) != specification.disk):
                    append_to_db.append(specification)

                # CPU RAM PROC Measurement
                cr_measurement = ps_out_to_dict(crm_ps1_response.std_out.decode())
                # print(cr_measurement)
                # print(cr_measurement)
                # add measurement
                append_to_db.append(
                    Info_Measurements(
                        server_id=host.id,
                        measurement_date=datetime.now(),
                        cpu_usage_pct=cr_measurement[0]['CPUUsagePercent'],
                        ram_used_pct=cr_measurement[0]['RAMUsedPercent']
                    )
                )
                for item in append_to_db:
                    db.session.add(item)
                db.session.commit()


def notification_check(host):
    append_to_db = []
    # Services
    watched_services = Spec_Service.query.filter_by(server_id=host.id, watched=1).all()
    for service in watched_services:
        last_status = sorted(service.info, key=lambda x: x.status_change_date, reverse=True)[0]
        last_notification = Notification.query.filter_by\
            (server_id=host.id, content=f'Service: {service.name} is {last_status.status}.', resolved=0).first()
        if last_status.status != 'Running':
            if not last_notification:
                print(last_notification)
                append_to_db.append(Notification(
                    content=f'Service: {service.name} is {last_status.status}.',
                    server_id=host.id,
                    cause_type='Service',
                    resolved=0,
                    date=datetime.now()
                ))
        elif last_notification:
            last_notification.resolved = 1

    # CPU
    # RAM
    avg_cpu_usage = 0
    avg_ram_usage = 0
    last_measurements = Info_Measurements.query.filter_by(server_id=host.id).\
        order_by(Info_Measurements.measurement_date.desc()).limit(5)
    for measurement in last_measurements:
        avg_cpu_usage += float(measurement.cpu_usage_pct)
        avg_ram_usage += float(measurement.ram_used_pct)
    avg_cpu_usage = avg_cpu_usage/5
    avg_ram_usage = avg_ram_usage/5
    last_cpu_notification = Notification.query.filter_by(server_id=host.id, cause_type='CPU usage', resolved=0).first()
    if avg_cpu_usage > 70:
        if not last_cpu_notification:
            append_to_db.append(Notification(
                content=f'CPU usage is {avg_cpu_usage}%.',
                server_id=host.id,
                cause_type='CPU usage',
                resolved=0,
                date=datetime.now()
            ))
    elif last_cpu_notification:
        last_cpu_notification.resolved = 1
    last_ram_notification = Notification.query.filter_by(server_id=host.id, cause_type='RAM usage', resolved=0).first()
    if avg_ram_usage > 70 :
        if not last_ram_notification:
            append_to_db.append(Notification(
                content=f'RAM usage is {avg_ram_usage}%.',
                server_id=host.id,
                cause_type='RAM usage',
                resolved=0,
                date=datetime.now()
            ))
    elif last_ram_notification:
        last_ram_notification.resolved = 1
    # DISK
    unique_disk_ids = db.session.query(Info_DiskMeasurements.disk_id).filter(
        Info_DiskMeasurements.server_id == host.id
    ).distinct().all()

    for disk in unique_disk_ids:
        last_measurement = Info_DiskMeasurements.query.filter_by(disk_id=disk.disk_id).\
            order_by(Info_DiskMeasurements.measurement_date.desc()).first()
        used_space = int(last_measurement.used_space)
        total_space = int(last_measurement.total_space)
        last_notification = Notification.query.filter_by \
            (server_id=host.id, cause_type=f'Disk {disk.disk_id} occupancy', resolved=0).first()
        if used_space/total_space > 0.7:
            if not last_notification:
                append_to_db.append(Notification(
                    content=f'Disk {disk.disk_id} is {round(used_space/total_space)*100}% occupied.',
                    server_id=host.id,
                    cause_type=f'Disk {disk.disk_id} occupancy',
                    resolved=0,
                    date=datetime.now()
                ))
        elif last_notification:
            last_notification.resolved = 1
    for item in append_to_db:
        db.session.add(item)
    db.session.commit()
def run():

    while True:
        remove = Servers.query.filter_by(remove=1).all()
        if len(remove) != 0:
            Servers.query.filter_by(remove=1).delete()
            db.session.commit()

        servers = Servers.query.all()
        if len(servers) != 0:
            with ThreadPoolExecutor(max_workers=len(servers)) as worker:
                servers_response = [worker.submit(wmi_check, server) for server in servers]
                for future in servers_response:
                    try:
                        server_data = future.result()
                    except Exception as e:
                        print(f'ERROR: {e}')
            for server in servers:
                notification_check(server)
            time.sleep(10)
        else:
            time.sleep(10)
            print('lack of servers')
