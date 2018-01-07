"------------------------------------------"
"Removing existing Python tools..."
"------------------------------------------"
pip uninstall virtualenv
pip uninstall pipenv
pip uninstall pew

"------------------------------------------"
"Installing Python tools..."
"------------------------------------------"
pip install virtualenv
pip install pipenv
pip install pew

"Press any key to continue..."
cmd /c pause | out-null