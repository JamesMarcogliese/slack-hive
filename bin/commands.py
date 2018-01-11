# -*- coding: utf-8 -*-
"""
A module for handling commands for the Hive Slack app 
"""
from datetime import datetime
from elasticsearch import Elasticsearch
import requests
from pathlib import Path
import re

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def saveNote(message):
	print ("SaveNote")
	
	query = {
		"query": {
			"filter": [
				{ "term": { "author": message['user'] }}
				]
			}
		}
	
	res = es.search(index="note-index", body=query)
	
	doc = {
		'note': message['text'].lstrip('save '),
		'author': message['user'],
		'frequency': 0,
		'team': 'rollout',
		'timestamp': datetime.now()
		}
	
	res = es.index(index="note-index", doc_type='note', body=doc) 
	es.indices.refresh(index="note-index")

	
	return "Note saved!"
	
	print (message)

def searchNote(message):
	print ("searchNote")
	message = message.lstrip('search ')

def setTeam(message):
	print ("setTeam")
	
	doc = {
		'author': message['user'],
		'team': message['text'].lstrip('team ')
		}
	
	res = es.index(index="author-index", doc_type='author', body=doc) 
	es.indices.refresh(index="person-index")

def help(message):
	print ("help")
	
def fallback(message):
	print ("fallback")
	return "Sorry, I dont understand."

def identifyCommand(event_data):
	message = event_data["event"]
	channel = message["channel"]
	messageText = message['text']
	patterns=['^save (.*)', '^search (.*)', '^team (.*)', '^help', '.*']
	functions=['saveNote', 'searchNote', 'setTeam', 'help', 'fallback']
	
	for idx, pattern in enumerate(patterns):
		if re.compile(patterns[idx]).search(messageText) is not None:
			return eval(functions[idx])(message)
		
if __name__ == '__main__':
	identifyCommand("test")