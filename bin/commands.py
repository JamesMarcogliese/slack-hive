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

def save_note(event_data):
	print ("SaveNote")
	
	#Search for author's team from author index
	query = {
			"query": {
				"match": {
					"author": event_data['event']['user'] 
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
		'note': event_data['event']['text'].lstrip('save '),
		'author': event_data['event'],
		'frequency': 0,
		'team': author['hits']['hits'][0]['_source']['team'],
		'timestamp': datetime.now()
		}
	
	es.index(index="note-index", doc_type='note', body=doc, refresh="true") 

	return "Note saved! :notebook:", None

def find_note(event_data):
	print ("findNote")
	message = event_data['event']['text'].lstrip('find ')

def set_team(event_data):
	print ("setTeam")
	
	if event_data["type"] == 'event_callback':
		# Send the list to the user
		menu = json.load(open('teams_menu.json'))
		return "What team do you belong to?", menu
	elif event_data["type"] == 'interactive_message':
		# Check the users selection
		user = event_data["user"]["id"]
		selected_team = event_data["actions"][0]["selected_options"][0]["value"]
	else:
		return "There's been a error.", None
		
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
			es.delete(index="author-index", doc_type='author', id=author['hits']['hits'][0]['_id'])
	
	doc = {
		'author': user,
		'team': selected_team
		}
	
	es.index(index="author-index", doc_type='author', body=doc, refresh="true") 
	
	return "You have set yourself on the " + selected_team + " team!", None

def review(event_data):
	print ("review")
	
def help(event_data):
	print ("help")
	return Path('help_menu.txt').read_text(), None 
	
def fallback(event_data):
	print ("fallback")
	return ":confounded: Sorry, I don't understand. Type 'help' to see a list of what I can do!", None

def identify_command(event_data):
	channel = event_data["event"]["channel"]
	message_text = event_data["event"]['text']
	patterns=['^save (.*)', '^find (.*)', '^team', '^help', '.*']
	functions=['save_note', 'find_note', 'set_team', 'help', 'fallback']
	
	for idx, pattern in enumerate(patterns):
		if re.compile(patterns[idx]).search(message_text) is not None:
			return eval(functions[idx])(event_data)
			
def identify_callback(action_data):
	callback_types=['team_selection']
	functions=['set_team']
	for idx, callback_type in enumerate(callback_types):
		if action_data["callback_id"] == callback_types[idx]:
			return eval(functions[idx])(action_data)