# Creating an empty .NET DataTable
$spec_os = New-Object System.Data.DataTable

# Adding columns to the DataTable
$spec_os.Columns.Add((New-Object System.Data.DataColumn 'OperatingSystemVersion|&', ([string])))
$spec_os.Columns.Add((New-Object System.Data.DataColumn 'OperatingSystemArchitecture|&', ([string])))

# Retrieving information about the operating system using WMI
$os_info = Get-WmiObject -Class Win32_OperatingSystem

# Adding information to the DataTable
foreach ($os in $os_info) {
    # Creating a new row
    $row = $spec_os.NewRow()

    # Setting row values
    $row['OperatingSystemVersion|&'] = "$($os.Caption)|&"
    $row['OperatingSystemArchitecture|&'] = "$($os.OSArchitecture)|&"

    # Adding the row to the table
    $spec_os.Rows.Add($row)
}

# Displaying the results as a table
$spec_os | Format-Table -AutoSize
