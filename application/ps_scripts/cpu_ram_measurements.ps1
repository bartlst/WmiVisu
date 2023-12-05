# Retrieving information about average CPU usage
$processor = Get-WmiObject -Class Win32_PerfFormattedData_PerfOS_Processor | Where-Object { $_.Name -eq '_Total' }
$average_processor_usage = [int]$processor.PercentProcessorTime

# Retrieving information about RAM
$os = Get-WmiObject -Class Win32_OperatingSystem
$total_physical_memory = [int]$os.TotalVisibleMemorySize
$free_physical_memory = [int]$os.FreePhysicalMemory
$used_memory = $total_physical_memory - $free_physical_memory
$used_memory_percentage = ($used_memory / $total_physical_memory) * 100

# Creating a DataTable to store information about CPU and RAM usage
$spec_ram = New-Object System.Data.DataTable

# Adding columns to the DataTable
$spec_ram.Columns.Add((New-Object System.Data.DataColumn 'CPUUsagePercent|&', ([string])))
$spec_ram.Columns.Add((New-Object System.Data.DataColumn 'RAMUsedPercent|&', ([string])))

# Creating a row with information about CPU and RAM usage
$row = $spec_ram.NewRow()
$row['CPUUsagePercent|&'] = "$($average_processor_usage)|&"
$row['RAMUsedPercent|&'] = "$([math]::Round($used_memory_percentage, 2))|&"

# Adding the row to the DataTable
$spec_ram.Rows.Add($row)

# Displaying the results as a table
$spec_ram | Format-Table -AutoSize
