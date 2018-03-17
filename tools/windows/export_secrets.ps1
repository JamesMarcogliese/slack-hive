"--------------------------------------------------"
"Exporting slack secrets to local environment..."
"--------------------------------------------------"
$env:SLACK_CLIENT_ID='#######'
$env:SLACK_CLIENT_SECRET='#######'
$env:SLACK_VERIFICATION_TOKEN='#######'
$env:SLACK_BOT_TOKEN='#######'

"Press any key to continue..."
cmd /c pause | out-null