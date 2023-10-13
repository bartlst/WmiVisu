import wmi

# Informacje o serwerze i uwierzytelnianiu
server = '192.168.153.129'
username = 'admin'
password = 'admin'

# Ustawienie połączenia WMI
connection = wmi.WMI(computer=server, user=username, password=password)

# Pobieranie informacji o systemie operacyjnym
for os_info in connection.Win32_OperatingSystem():
    print("---- OS Information ----")
    print(f"Server Name: {server}")
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

# ... Podobne wydruki dla innych kategorii informacji