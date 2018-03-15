# make sure ES is up and running
#import requests
#res = requests.get('http://localhost:9200')
#print(res.content)

#connect to our cluster
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import json
import requests
import csv
records = []

if (es.indices.exists(index="note-index")):
	es.indices.delete(index="note-index")
	
if (es.indices.exists(index="author-index")):
	es.indices.delete(index="author-index")

doc = {
	'author': 'U8GQW24TY',
	'team': 'rollout'
	}
	
doc = {
	'author': 'U8GQW24TY',
	'team': 'rollout'
	}

res = es.index(index="author-index", doc_type='author', body=doc) 
es.indices.refresh(index="author-index")	
	
dt = datetime.now()
unix_time = time.mktime(dt.timetuple())

with open('testData1.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        records.append(row[0])

for note in (records):		
# Save note to note-index
	doc = {
		'note': note,
		'author': "U8GQW24TY",
		'frequency': 0,
		'team': "rollout",
		'timestamp': unix_time
		}
	res = es.index(index="note-index", body=doc) 
	
records = []	
with open('testData2.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        records.append(row[0])
		
for note in (records):		
# Save note to note-index
	doc = {
		'note': note,
		'author': "U8GQW24TY",
		'frequency': 0,
		'team': "rollout",
		'timestamp': unix_time
		}
	res = es.index(index="note-index", body=doc) 

#res = es.search(index="author-index", body=query)

#if (res['hits']['hits'][0]['_source']['team']) is None:
#	print ("Hey yo")

#parsed = json.loads(res)
#print (json.dumps(parsed, indent=4, sort_keys=True))

#res = es.index(index="note-index", doc_type='note', body=doc1) 

#res = es.index(index="person-index", doc_type='person', body=doc2) 

#es.indices.refresh(index="note-index")
#es.indices.refresh(index="person-index")

#res = es.search(index="note-index", body={"query": {"match_all": {}}})
#print("Got %d Hits:" % res['hits']['total'])
#for hit in res['hits']['hits']:
#    print("%(timestamp)s %(author)s: %(note)s" % hit["_source"])

