& .\stop_elk.ps1
& .\remove_elk.ps1
invoke-expression 'cmd /c start powershell -Command { .\launch_ngrok.ps1 }'
invoke-expression 'cmd /c start powershell -Command { .\start_elk.ps1 }'
invoke-expression 'cmd /c start powershell -Command { .\start_server.ps1 }'