# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import json
import sys
sys.path.append('../')
from utilities import globals

def pattern():
	return '^team'
	
def execute_event(event_data):
	print ("setTeam")
	print (event_data)
	if event_data["type"] == 'event_callback':
		# Send the list to the user
		teams_menu = json.load(open('./resources/teams_menu.json'))
		channel = event_data["event"]["channel"]
		globals.slack_client.api_call("chat.postMessage", channel=channel, text="What team do you belong to?", attachments=teams_menu)
		return
	elif event_data["type"] == 'interactive_message':
		# Check the users selection
		user = event_data["user"]["id"]
		selected_team = event_data["actions"][0]["selected_options"][0]["value"]
		channel = event_data["channel"]["id"]
		
	#Search for author's team from author index
	query = {
			"query": {
				"match": { 
					"author": user 
				}
			}
		}
		
	if (globals.es.indices.exists(index="author-index")):
		author = globals.es.search(index="author-index", body=query)	
		print (author)
		if (author['hits']['total'] != 0):
			globals.es.delete(index="author-index", doc_type='author', id=author['hits']['hits'][0]['_id'])
			print ("Deleted")
	
	doc = {
		'author': user,
		'team': selected_team
		}
	
	globals.es.index(index="author-index", doc_type='author', body=doc, refresh="true") 
	
	message = "You are now sharing notes with the " + selected_team + " team!"
	globals.slack_client.api_call("chat.update", channel=channel, ts=event_data["message_ts"], text=message, attachments=[])
	return