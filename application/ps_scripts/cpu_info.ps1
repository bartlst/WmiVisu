# Retrieving information about the CPU
$cpu_info = Get-WmiObject -Class Win32_Processor

# Creating a DataTable to store information about CPU
$spec_cpu = New-Object System.Data.DataTable

# Adding columns to the DataTable
$spec_cpu.Columns.Add((New-Object System.Data.DataColumn 'CPUName|&', ([string])))
$spec_cpu.Columns.Add((New-Object System.Data.DataColumn 'Manufacturer|&', ([string])))
$spec_cpu.Columns.Add((New-Object System.Data.DataColumn 'NumberOfCores|&', ([string])))
$spec_cpu.Columns.Add((New-Object System.Data.DataColumn 'NumberOfLogicalProcessors|&', ([string])))

# Creating a row with information about the CPU
foreach ($cpu in $cpu_info) {
    $row = $spec_cpu.NewRow()
    $row['CPUName|&'] = "$($cpu.Name)|&"
    $row['Manufacturer|&'] = "$($cpu.Manufacturer)|&"
    $row['NumberOfCores|&'] = "$($cpu.NumberOfCores)|&"
    $row['NumberOfLogicalProcessors|&'] = "$($cpu.NumberOfLogicalProcessors)|&"

    # Adding the row to the DataTable
    $spec_cpu.Rows.Add($row)
}

# Displaying the results as a table
$spec_cpu | Format-Table -AutoSize
