# Retrieving information about the motherboard using WMI
$board_info = Get-WmiObject -Class Win32_BaseBoard

# Retrieving information about the BIOS using WMI
$bios_info = Get-WmiObject -Class Win32_BIOS

# Creating a DataTable to store information about the motherboard
$spec_motherboard = New-Object System.Data.DataTable

# Adding columns to the DataTable
$spec_motherboard.Columns.Add((New-Object System.Data.DataColumn 'MotherboardManufacturer|&', ([string])))
$spec_motherboard.Columns.Add((New-Object System.Data.DataColumn 'MotherboardModel|&', ([string])))
$spec_motherboard.Columns.Add((New-Object System.Data.DataColumn 'BiosVersion|&', ([string])))

# Assigning values to variables
$manufacturer = $board_info.Manufacturer
$model = $board_info.Product
$bios_versions = $bios_info | Select-Object -ExpandProperty Version

# Concatenating all BIOS versions if there is more than one
$bios_version = $bios_versions -join " / "

# Creating a row for the motherboard information and BIOS
$row = $spec_motherboard.NewRow()
$row['MotherboardManufacturer|&'] = "$($manufacturer)|&"
$row['MotherboardModel|&'] = "$($model)|&"
$row['BiosVersion|&'] = "$($bios_version)|&"

# Adding the row to the DataTable
$spec_motherboard.Rows.Add($row)

# Displaying the results as a table
$spec_motherboard | Format-Table -AutoSize
