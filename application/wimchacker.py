import wmi
import logging
from concurrent.futures import ThreadPoolExecutor
import sys
import time
import pythoncom

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# def handle_exception(exc_type, exc_value, exc_traceback):
#     logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
#
#
# sys.excepthook = handle_exception


# Informacje o serwerze i uwierzytelnianiu
USERNAME = 'admin'
PASSWORD = 'admin'

# Ustawienie połączenia WMI
# connection = wmi.WMI(computer=SERVER, user=USERNAME, password=PASSWORD)




def  Client_WMI_check(computer):
    pythoncom.CoInitialize()
    try:
        connection = wmi.WMI(computer=computer, user=USERNAME, password=PASSWORD)
    except wmi.x_wmi as e:
        logging.error(f"{computer}: {e}")
        print(f"{computer}: {e}")
        pythoncom.CoUninitialize()
        exit()

    # specification

    # Pobieranie informacji o systemie operacyjnym
    for os_info in connection.Win32_OperatingSystem():
        print("---- OS Information ----")
        print(f"Server Name: {computer}")
        print(f"OS Name & Version: {os_info.Caption}")
        print(f"Architecture: {os_info.OSArchitecture}")
        print(f"Install Date: {os_info.InstallDate}")
        print(f"Last Boot Up Time: {os_info.LastBootUpTime}")
        print("-------------------------\n")

    # Pobieranie informacji o płycie głównej
    for motherboard in connection.Win32_BaseBoard():
        print("---- Motherboard Information ----")
        print(f"Manufacturer: {motherboard.Manufacturer}")
        print(f"Model: {motherboard.Product}")
        print(f"BIOS Version: {motherboard.Version}")
        print("---------------------------------\n")

    # Pobieranie informacji o kartach graficznych
    for gpu in connection.Win32_VideoController():
        print("---- GPU Information ----")
        print(f"Name: {gpu.Name}")
        print(f"Memory Size (GB): {float(gpu.AdapterRAM) / (1024 ** 3)}")
        print(f"Driver Version: {gpu.DriverVersion}")
        print("-------------------------\n")

    # Pobieranie informacji o interfejsach sieciowych
    for network_interface in connection.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        print("---- Network Interface Information ----")
        print(f"Interface Name: {network_interface.Description}")
        print(f"IP Address: {network_interface.IPAddress[0] if network_interface.IPAddress else 'N/A'}")
        print(f"Subnet Mask: {network_interface.IPSubnet[0] if network_interface.IPSubnet else 'N/A'}")
        print(f"Gateway: {network_interface.DefaultIPGateway[0] if network_interface.DefaultIPGateway else 'N/A'}")
        print(f"MAC Address: {network_interface.MACAddress}")
        print("--------------------------------------\n")

    for disk in connection.Win32_DiskDrive():
        print("---- Disk Information ----")
        print(f"Disk Name: {disk.DeviceID}")
        print(f"Disk Interface: {disk.InterfaceType}")
        print(f"Disk Type: {disk.MediaType}")
        print(f"Disk Size (GB): {float(disk.Size)/1073741824:.2f}")
        print("-------------------------\n")

    pythoncom.CoUninitialize()



servers = ['192.168.153.129']
while True:
    with ThreadPoolExecutor(max_workers=len(servers)) as worker:
        futures = [worker.submit(Client_WMI_check, server) for server in servers]

    time.sleep(10)