# -*- coding: utf-8 -*-
"""
A module for handling commands for the Hive Slack app 
"""
from elasticsearch import Elasticsearch
from datetime import datetime
from pathlib import Path
import requests
import json
import re


# Connect to Elasticsearch instance
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def save_note(message):
	print ("SaveNote")
	
	#Search for author's team from author index
	query = {
			"query": {
				"match": {
					"author": message['user'] 
				}
			}
		}
	if (es.indices.exists(index="author-index")):
		author = es.search(index="author-index", body=query)
	
	if (author['hits']['total'] == 0) or not(es.indices.exists(index="author-index")):
		return """Wait! :raised_hand:I need to know what team you're on before I can save your notes! 
				  Please set your team by using the 'team' command!"""
	
	# Save note to note-index
	doc = {
		'note': message['text'].lstrip('save '),
		'author': message['user'],
		'frequency': 0,
		'team': author['hits']['hits'][0]['_source']['team'],
		'timestamp': datetime.now()
		}
	
	es.index(index="note-index", doc_type='note', body=doc, refresh="true") 

	return "Note saved! :notebook:", None

def find_note(message):
	print ("findNote")
	message = message.lstrip('find ')

def set_team(message):
	print ("setTeam")
	
	if message["type"] is not None and message["type"] is not "interactive_message":
		# Send the list to the user
		menu = json.load(open('teams_menu.json'))
		return "What team do you belong to?",menu
	else:
		# Check the users selection
		user = message_action["user"]["id"]
		selected_team = message["actions"][0]["selected_options"][0]["value"]
		
	#Search for author's team from author index
	query = {
			"query": {
				"match": {
					"author": user 
				}
			}
		}
	if (es.indices.exists(index="author-index")):
		author = es.search(index="author-index", body=query)	
		if (author['hits']['total'] != 0):
			es.delete(index="author-index", id=author['hits']['hits'][0]['_id'])
	
	doc = {
		'author': user,
		'team': selected_team
		}
	
	es.index(index="author-index", doc_type='author', body=doc, refresh="true") 
	
	return "Team set!"

def review(message):
	print ("review")
	
def help(message):
	print ("help")
	return Path('help_menu.txt').read_text(), None 
	
def fallback(message):
	print ("fallback")
	return ":confounded: Sorry, I don't understand. Type 'help' to see a list of what I can do!", None

def identify_command(event_data):
	message = event_data["event"]
	channel = message["channel"]
	message_text = message['text']
	patterns=['^save (.*)', '^find (.*)', '^team', '^help', '.*']
	functions=['save_note', 'find_note', 'set_team', 'help', 'fallback']
	
	for idx, pattern in enumerate(patterns):
		if re.compile(patterns[idx]).search(message_text) is not None:
			return eval(functions[idx])(message)