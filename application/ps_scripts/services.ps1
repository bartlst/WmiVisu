# Retrieving information about services using WMI
$services = Get-WmiObject -Class Win32_Service

# Creating a DataTable to store information about services
$services_list = New-Object System.Data.DataTable

# Adding columns to the DataTable
$services_list.Columns.Add((New-Object System.Data.DataColumn 'Name|&', ([string])))
$services_list.Columns.Add((New-Object System.Data.DataColumn 'Status|&', ([string])))
$services_list.Columns.Add((New-Object System.Data.DataColumn 'StartMode|&', ([string])))

# Iterating through each service and retrieving its name and state
foreach ($service in $services) {
    # Creating a row for each service
    $row = $services_list.NewRow()
    $row['Name|&'] = "$($service.Name)|&"
    $row['Status|&'] = "$($service.State)|&"
    $row['StartMode|&'] = "$($service.StartMode)|&"

    # Adding the row to the DataTable
    $services_list.Rows.Add($row)
}

# Displaying the results as a table
$services_list | Format-Table -AutoSize
