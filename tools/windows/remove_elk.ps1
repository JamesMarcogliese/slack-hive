"------------------------------------------"
"Stopping Docker ELK container..."
"------------------------------------------"
docker stop elk
"------------------------------------------"
"Removing stopped Docker ELK container..."
"------------------------------------------"
docker rm elk

"Press any key to continue..."
cmd /c pause | out-null