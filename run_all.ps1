# Custom python env
$py_env = '../aoc2023/Scripts/python.exe'

# Get the current directory
$base_dir = Get-Location

# Get the directories that match the pattern
$directories = Get-ChildItem -Directory -Name 'day*'

# Get the number of directories
$number_of_directories = ($directories | Measure-Object).Count

# Specify the timeout limit in seconds
$timeout_limit = 10 * 1000  # PowerShell uses milliseconds for timeout

# Long execution time tasks
$long_execution_time_tasks = 5, 17, 23
# Iterate through the directories
for ($i = 1; $i -le $number_of_directories; $i++) {
    $folder = "day${i}"  # Create the folder name

    if ($long_execution_time_tasks -contains $i) {
        Write-Host "Skipping day $i solution..." -ForegroundColor Yellow
        Write-Host "Reason: long execution time" 
        Write-Host "Run manually if needed."
        continue
    }

    # Change to the directory
    Set-Location -Path $folder

    # Print the message
    Write-Host "Running day $i solution..." -ForegroundColor Green

    # Start the process and measure its execution time
    $executionTime = Measure-Command {
        $process = Start-Process -FilePath $py_env -ArgumentList 'solution.py' -PassThru -NoNewWindow
        # Wait for the process to complete or timeout
        if (-not $process.WaitForExit($timeout_limit)) {
            Write-Host "Script execution exceeded ${timeout_limit} ms. Killing the process." -ForegroundColor Red
            Stop-Process -Id $process.Id -Force
        }
    }

    Write-Host "Execution time: $([math]::Round($executionTime.TotalMilliseconds, 2)) ms"

    # Change back to the base directory
    Set-Location -Path $base_dir
}