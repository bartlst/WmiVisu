Clear-Host

# Retrieving information about RAM
$os = Get-WmiObject -Class Win32_OperatingSystem
$total_physical_memory = [math]::Round($os.TotalVisibleMemorySize / 1024 / 1024, 2) # Total physical memory in GB


# Creating a DataTable to store information about RAM
$spec_ram = New-Object System.Data.DataTable

# Adding columns to the DataTable
$spec_ram.Columns.Add((New-Object System.Data.DataColumn 'TotalMemoryGB|&', ([string])))

# Creating a row with information about RAM
$row = $spec_ram.NewRow()
$row['TotalMemoryGB|&'] = "$($total_physical_memory)GB|&"

# Adding the row to the DataTable
$spec_ram.Rows.Add($row)

# Displaying the results as a table
$spec_ram | Format-Table -AutoSize
