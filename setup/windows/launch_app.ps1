"------------------------------------------------------"
"Lauching the flask server ..."
"------------------------------------------------------"
& .\export_slack_secrets.ps1
cd..
cd..
pipenv run python app.py

"Press any key to continue..."
cmd /c pause | out-null