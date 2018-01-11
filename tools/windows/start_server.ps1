"------------------------------------------------------"
"Launching the flask server ..."
"------------------------------------------------------"
& .\export_secrets.ps1
cd..
cd..
cd bin
pipenv run python app.py

"Press any key to continue..."
cmd /c pause | out-null