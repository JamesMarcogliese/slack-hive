invoke-expression 'cmd /c start powershell -Command { .\export_slack_secrets.ps1 }'
invoke-expression 'cmd /c start powershell -Command { .\launch_ngrok.ps1 }'
invoke-expression 'cmd /c start powershell -Command { .\start_elk.ps1 }'
invoke-expression 'cmd /c start powershell -Command { .\launch_app.ps1 }'