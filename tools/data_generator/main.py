# Quick and dirty data generator for testing
# Inserts data into ES indexes

#connect to our cluster
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import requests
import csv
import time

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
records = []

if (es.indices.exists(index="note-index")): # Check if index exists
	es.indices.delete(index="note-index")
	
if (es.indices.exists(index="author-index")):
	es.indices.delete(index="author-index")

doc1 = {	# User one
	'author': 'U8GQW24TY',
	'team': 'rollout'
	}
	
doc2 = { # User two
	'author': 'U8GQW26TY',
	'team': 'rollout'
	}

res = es.index(index="author-index", doc_type='author', body=doc1) # Insert users
res = es.index(index="author-index", doc_type='author', body=doc2) 
	
dt = datetime.now()
unix_time = time.mktime(dt.timetuple())

with open('testData1.csv') as csvDataFile:	# Read Files
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        records.append(row[0])

for note in (records):		# Generate logs and insert
# Save note to note-index
	doc = {
		'note': note,
		'author': "U8GQW24TY",
		'frequency': 0,
		'team': "rollout",
		'timestamp': unix_time
		}
	res = es.index(index="note-index", doc_type='note', body=doc) 
	
records = []	
with open('testData2.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        records.append(row[0])
		
for note in (records):		
# Save note to note-index
	doc = {
		'note': note,
		'author': "U9QQTDEF7",
		'frequency': 0,
		'team': "rollout",
		'timestamp': unix_time
		}
	res = es.index(index="note-index", doc_type='note', body=doc) 

#parsed = json.loads(res)
#print (json.dumps(parsed, indent=4, sort_keys=True))

es.indices.refresh(index="note-index")	# Refresh Indexes
es.indices.refresh(index="author-index")	