$projectDir = $PSScriptRoot
$taskName   = "GitHubIssueCalendarSync"

$action = New-ScheduledTaskAction `
    -Execute "uv" `
    -Argument "run src/main.py" `
    -WorkingDirectory $projectDir

# Alle 2 Stunden, beginning heute um Mitternacht
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 2) -Once -At "00:00"

# Headless: kein Fenster, im Hintergrund
$settings = New-ScheduledTaskSettingsSet `
    -Hidden `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName   $taskName `
    -Action     $action `
    -Trigger    $trigger `
    -Settings   $settings `
    -RunLevel   Highest `
    -Description "Sync GitHub Issues to Google Tasks alle 2 Stunden" `
    -Force

Write-Host "Task '$taskName' erfolgreich registriert."
Write-Host "Naechste Ausfuehrungen: alle 2 Stunden."
