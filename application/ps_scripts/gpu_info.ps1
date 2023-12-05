# Retrieving information about video cards using WMI
$video_cards = Get-WmiObject -Class Win32_VideoController

# Creating a DataTable to store information about GPUs
$spec_gpu = New-Object System.Data.DataTable

# Adding columns to the DataTable
$spec_gpu.Columns.Add((New-Object System.Data.DataColumn 'GPUName|&', ([string])))
$spec_gpu.Columns.Add((New-Object System.Data.DataColumn 'MemorySizeInGB|&', ([string])))
$spec_gpu.Columns.Add((New-Object System.Data.DataColumn 'DriverVersion|&', ([string])))

# Iterating through each video card and retrieving information
foreach ($video_card in $video_cards) {
    $gpu_name = $video_card.Name
    $gpu_memory_size = [math]::Round($video_card.AdapterRAM / 1024 / 1024 / 1024)
    $gpu_driver_version = $video_card.DriverVersion

    # Creating a row for each video card
    $row = $spec_gpu.NewRow()
    $row['GPUName|&'] = "$($gpu_name)|&"
    $row['MemorySizeInGB|&'] = "$($gpu_memory_size)GB|&"
    $row['DriverVersion|&'] = "$($gpu_driver_version)|&"

    # Adding the row to the DataTable
    $spec_gpu.Rows.Add($row)
}

# Displaying the results as a table
$spec_gpu | Format-Table -AutoSize
