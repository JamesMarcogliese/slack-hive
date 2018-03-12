# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import sys
sys.path.append('../')
from utilities import globals
from datetime import datetime
import time

def pattern():
	return '^save (.*)'

def execute_event(event_data):
	print ("SaveNote")
	channel = event_data["event"]["channel"]
	
	#Search for author's team from author index
	query = {
			"query": {
				"match": {
					"author": event_data['event']['user'] 
				}
			}
		}
		
	if (globals.es.indices.exists(index="author-index")):
		author = globals.es.search(index="author-index", body=query)
	else:
		print ("No author index could be found!")
		
	if (author['hits']['total'] == 0):
		message = ("Wait! :raised_hand: I need to know what team you're on before I can save your notes!\n" 
				   "Please set your team by using the 'team' command!"
				   )
		globals.slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
		return 
	
	dt = datetime.now()
	unix_time = time.mktime(dt.timetuple())
	
	# Save note to note-index
	doc = {
		'note': event_data["event"]["text"].lstrip("save "),
		'author': event_data["event"]["user"],
		'frequency': 0,
		'team': author["hits"]["hits"][0]["_source"]["team"],
		'timestamp': unix_time
		}
	
	globals.es.index(index="note-index", doc_type="note", body=doc, refresh="true") 

	globals.slack_client.api_call("chat.postMessage", channel=channel, text="Note saved!", attachments=None)
	return