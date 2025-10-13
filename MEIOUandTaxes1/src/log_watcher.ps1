# Path to your game.log
$gameLog = "C:\Users\????\Documents\Paradox Interactive\Europa Universalis IV\logs\game.log"

# Path for the output file
$outputFile = "C:\Users\????\Documents\Paradox Interactive\Europa Universalis IV\logs\game_time.log"

# Start watching the log
Get-Content $gameLog -Wait | ForEach-Object {
    # Add system timestamp in HH:mm:ss.fff format
    $timestampedLine = "$(Get-Date -Format 'HH:mm:ss.fff') $_"

    # Append to run.txt
    $timestampedLine | Out-File $outputFile -Append
}