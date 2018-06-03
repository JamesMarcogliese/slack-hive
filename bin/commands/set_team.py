# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import json
import sys
sys.path.append('../')
from utilities import globals
from utilities import es_queries
import classes

def pattern():
	return '^team'
	
def execute_event(event_data):
	print ("setTeam")
	print (event_data)
	if event_data["type"] == 'event_callback':
		# Send the team list to the user
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
	author = es_queries.get_team(user)
	if (author is not None):
		es_queries.delete_author_doc(author.doc_id)
	es_queries.add_author(user, selected_team)
	
	message = "You are now sharing notes with the " + selected_team + " team!"
	globals.slack_client.api_call("chat.update", channel=channel, ts=event_data["message_ts"], text=message, attachments=[])
	return