# Pobieranie informacji o dyskach twardych za pomocą WMI
$disks = Get-WmiObject -Class Win32_LogicalDisk -Filter "DriveType = 3"

# Tworzenie DataTable do przechowywania informacji o dyskach
$spec_disk = New-Object System.Data.DataTable

# Dodawanie kolumn do DataTable
$spec_disk.Columns.Add((New-Object System.Data.DataColumn 'DiskID|&', ([string])))
$spec_disk.Columns.Add((New-Object System.Data.DataColumn 'TotalSizeB|&', ([string])))
$spec_disk.Columns.Add((New-Object System.Data.DataColumn 'UsedSpaceB|&', ([string])))
$spec_disk.Columns.Add((New-Object System.Data.DataColumn 'FreeSpaceB|&', ([string])))

# Iterowanie przez każdy dysk i pobieranie jego ID, całkowitej i wolnej przestrzeni
foreach ($disk in $disks) {
    if ($disk.Size -and $disk.FreeSpace) {
        $total_space = $disk.Size
        $free_space = $disk.FreeSpace
        $used_space = $total_space - $free_space

        # Tworzenie wiersza dla każdego dysku
        $row = $spec_disk.NewRow()
        $row['DiskID|&'] = "$($disk.DeviceID)|&"
        $row['TotalSizeB|&'] = "$($total_space)|&"
        $row['UsedSpaceB|&'] = "$($used_space)|&"
        $row['FreeSpaceB|&'] = "$($free_space)|&"

        # Dodawanie wiersza do DataTable
        $spec_disk.Rows.Add($row)
    }
}

# Wyświetlanie wyników jako tabeli
$spec_disk | Format-Table -AutoSize