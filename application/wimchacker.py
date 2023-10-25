import wmi
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import date
import pythoncom
from website.models import *
from datetime import datetime, timedelta, timezone


def convert_cim_date(cim_date_str):
    year = int(cim_date_str[:4])
    month = int(cim_date_str[4:6])
    day = int(cim_date_str[6:8])
    hour = int(cim_date_str[8:10])
    minute = int(cim_date_str[10:12])
    second = int(cim_date_str[12:14])

    dt = datetime(year, month, day, hour, minute, second)

    return dt


USERNAME = 'admin'
PASSWORD = 'admin'
app = None
db = None


def Client_WMI_check(host):
    pythoncom.CoInitialize()
    with app.app_context():
        try:
            connection = wmi.WMI(computer=host.hostname)
            host.connection_status = 1
        except wmi.x_wmi as e:
            print(e)
            host.connection_status = 0
            pythoncom.CoUninitialize()
            return

        gpu_list = []
        disk_list = []
        # specification
        for info in connection.Win32_ComputerSystem():
            pass
            # print(info.name)

        # OS

        for os_info in connection.Win32_OperatingSystem():
            os_name_version = os_info.Caption
            architecture = os_info.OSArchitecture
            install_date = convert_cim_date(os_info.InstallDate)
            last_update = datetime.now()

        spec_os = Spec_OS(
            server_id=host.id,
            os_name_version=os_name_version,
            architecture=architecture,
            install_date=install_date,
            last_update=last_update
        )

        if len(host.os_specs) == 0:
            db.session.add(spec_os)
            db.session.commit()
        else:
            last_insert = host.os_specs[-1]
            if last_insert.os_name_version != spec_os.os_name_version:
                if last_insert.architecture != spec_os.architecture:
                    if last_insert.install_date != spec_os.install_date:
                        db.session.add(spec_os)
                        db.session.commit()

        # Motherboard

        for board in connection.Win32_BaseBoard():
            manufacturer = board.Manufacturer
            model = board.Product
        for bios in connection.Win32_BIOS():
            bios_version = bios.Version

        motherboard = Spec_Motherboard(
            server_id=host.id,
            manufacturer=manufacturer,
            model=model,
            bios_version=bios_version
        )
        if len(host.motherboards) == 0:
            db.session.add(motherboard)
            db.session.commit()
        else:
            last_insert = host.motherboards[-1]
            if last_insert.manufacturer != motherboard.manufacturer:
                if last_insert.model != motherboard.model:
                    if last_insert.bios_version != motherboard.bios_version:
                        db.session.add(motherboard)
                        db.session.commit()

        # GUP

        for video_card in connection.Win32_VideoController():
            gpu_name = video_card.Name
            gpu_memory_size = float(video_card.AdapterRAM) / (1024 ** 2)
            gpu_driver_version = video_card.DriverVersion

            gpu_list.append({
                "gpu_name": gpu_name,
                "gpu_memory_size": gpu_memory_size,
                "gpu_driver_version": gpu_driver_version
            })
        if len(host.gpus) == 0:
            for gpu in gpu_list:
                spec_gpu = Spec_GPU(
                    server_id=host.id,
                    name=gpu['gpu_name'],
                    memory_size=gpu['gpu_memory_size'],
                    driver_version=gpu['gpu_driver_version'],
                )
                db.session.add(spec_gpu)
                db.session.commit()
        else:
            for gpu in gpu_list:
                existing_gpu = next((x for x in host.gpus if (x.name == gpu['gpu_name']
                                                              or x.memory_size == gpu['gpu_memory_size']
                                                              or x.driver_version == gpu['gpu_driver_version'])), None)

                if not existing_gpu:
                    spec_gpu = Spec_GPU(
                        server_id=host.id,
                        name=gpu['gpu_name'],
                        memory_size=gpu['gpu_memory_size'],
                        driver_version=gpu['gpu_driver_version'],
                    )
                    db.session.add(spec_gpu)
                    db.session.commit()

        # Networks adapters

        # network_adapter_list = []
        #
        # for adapter in connection.Win32_NetworkAdapter():
        #     adapter_name = adapter.Name
        #     mac_address = adapter.MACAddress
        #
        #     network_adapter_list.append({
        #         "adapter_name": adapter_name,
        #         "mac_address": mac_address
        #     })
        #
        # if len(host.networkAdapters) == 0:
        #     for adapter in network_adapter_list:
        #         spec_adapter = Spec_NetworkAdapter(
        #             server_id=host.id,
        #             name=adapter['adapter_name'],
        #
        #             mac_address=adapter['mac_address'],
        #         )
        #         db.session.add(spec_adapter)
        #         db.session.commit()
        #
        # else:
        #     for adapter in network_adapter_list:
        #         existing_adapter = next((x for x in host.networkAdapters if (x.name == adapter['adapter_name']
        #                                                                       or x.mac_address == adapter[
        #                                                                           'mac_address'])), None)
        #
        #         if not existing_adapter:
        #             spec_adapter = Spec_NetworkAdapter(
        #                 server_id=host.id,
        #                 name=adapter['adapter_name'],
        #                 mac_address=adapter['mac_address'],
        #             )
        #             db.session.add(spec_adapter)
        #             db.session.commit()
        #
        # for adapter in connection.Win32_PerfRawData_Tcpip_NetworkInterface():
        #     matching_adapter = next((a for a in host.networkAdapters if a.name == adapter.Name), None)
        #     print('+')
        #     if matching_adapter:
        #         usage = NetworkAdapterUsage(
        #             adapter_id=matching_adapter.id,
        #             bytes_sent=adapter.BytesSentPerSec,
        #             bytes_received=adapter.BytesReceivedPerSec
        #         )
        #         # print(usage)
        #         db.session.add(usage)
        #         db.session.commit()
        #         print('a')

        for service in connection.Win32_Service():
            check_service = Info_Service.query.filter_by(name=service.Name).first()
            if not check_service:
                new_service = Info_Service(
                    server_id=host.id,
                    name=service.Name,
                    status=service.State,
                    status_change_date=datetime.now()
                )
                db.session.add(new_service)
            elif check_service.status != service.State:
                new_service = Info_Service(
                    server_id=host.id,
                    name=service.Name,
                    status=service.State,
                    status_change_date=datetime.now()
                )
                db.session.add(new_service)


        # DISK

        for disk in connection.Win32_LogicalDisk(DriveType=3):
            if disk.Size and disk.FreeSpace:
                total_space = float(disk.Size)
                free_space = float(disk.FreeSpace)
                used_space = total_space - free_space


                newDiskMeasurements = Info_DiskMeasurements(
                    server_id=host.id,
                    disk_id=disk.DeviceID,
                    total_space=total_space,
                    used_space=used_space,
                    free_space=free_space
                )
                db.session.add(newDiskMeasurements)
                db.session.commit()

        # RAM CPU

        for processor in connection.Win32_PerfFormattedData_PerfOS_Processor():
            if processor.Name == "_Total":
                average_processor_usage = int(processor.PercentProcessorTime)
                break

        # Pobieranie informacji o zużyciu RAMu
        for os in connection.Win32_OperatingSystem():
            total_physical_memory = int(os.TotalVisibleMemorySize)
            free_physical_memory = int(os.FreePhysicalMemory)
            used_memory = total_physical_memory - free_physical_memory
            used_memory_percentage = (used_memory / total_physical_memory) * 100

        new_measurement = Info_Measurements(
            server_id=host.id,
            measurement_date=datetime.now(),
            cpu_usage_pct=average_processor_usage,
            ram_used_pct=round(used_memory_percentage, 2)
        )

        db.session.add(new_measurement)
        db.session.commit()

        pythoncom.CoUninitialize()


def run():
    db.session.commit()
    while True:
        servers = Servers.query.all()
        if len(servers) != 0:
            # Client_WMI_check(servers[0])
            with ThreadPoolExecutor(max_workers=len(servers)) as worker:
                futures = [worker.submit(Client_WMI_check, server) for server in servers]

            # Po zakończeniu wszystkich wątków dokonujemy zapisu w bazie danych.
            db.session.commit()

            time.sleep(10)
        else:
            time.sleep(10)

            print('lack of servers')
