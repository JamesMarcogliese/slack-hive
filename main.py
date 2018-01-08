# make sure ES is up and running
#import requests
#res = requests.get('http://localhost:9200')
#print(res.content)

#connect to our cluster
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

if (es.indices.exists(index="test-index")):
	es.indices.delete(index="test-index")
	
if (es.indices.exists(index="note-index")):
	es.indices.delete(index="note-index")
	
if (es.indices.exists(index="person-index")):
	es.indices.delete(index="person-index")

doc1 = {
	'note': 'After database rebuild, remember to delete and reindex jobs!',
	'author': 'James Marcogliese',
	'frequency': '0',
	'team': 'rollout',
	'timestamp': datetime.now()
	}

doc2 = {
	'author': 'James Marcogliese',
	'team': 'rollout'
	}	

#res = es.index(index="note-index", doc_type='note', body=doc1) 

#res = es.index(index="person-index", doc_type='person', body=doc2) 

es.indices.refresh(index="note-index")
es.indices.refresh(index="person-index")

res = es.search(index="note-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(note)s" % hit["_source"])