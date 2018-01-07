"------------------------------------------"
"Pulling the lastest ELK container image..."
"------------------------------------------"
docker pull sebp/elk
"------------------------------------------"
"Starting ELK container..."
"------------------------------------------"
$cmdOutput = docker ps -a -f "name=elk"

If ($cmdOutput -contains 'elk') {
docker start elk
} Else{
docker run -p 5601:5601 -p 9200:9200 -p 5044:5044 -it -e LOGSTASH_START=0 -e KIBANA_START=1 -v elk-data:/var/lib/elasticsearch --name elk sebp/elk
}

cmd /c pause | out-null
