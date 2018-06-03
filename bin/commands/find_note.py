# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import sys
import re
sys.path.append('../')
from utilities import globals
from utilities import es_queries
import classes


def pattern():
	return '^find (.*)'

def execute_event(event_data):
	print ("findNote")
	pattern = re.compile('^find ')
	message = pattern.sub('', event_data['event']['text'])
	user = event_data['event']['user'] 
	channel = event_data["event"]["channel"]	

	#Search for author's team from author index
	author = es_queries.get_team(user)
		
	if (author is None):
		message = ("Wait! :raised_hand:I need to know what team you're on before I can search for notes!\n" 
				   "Please set your team by using the 'team' command!"
				   )
		globals.slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
		return 
		
	own_notes = es_queries.search_user_notes(author.author, message)
	team_notes = es_queries.search_team_notes(author.author, author.team, message)
		
	attachments = [] # --------------------------------------------------------------------------
	
	if (len(own_notes) >= 4):
		user_idx = 4
	elif (len(own_notes) == 0):
		user_idx = 0
	else:
		user_idx = len(own_notes)
		
	if (len(team_notes) >= 4):
		team_idx = 4
	elif (len(team_notes) == 0):
		team_idx = 0
	else:
		team_idx = len(team_notes)
		
	for idx in range(user_idx):	# The following two loops should be condensed
		record = {}

		print ("User record " + str(idx))
		record["color"] = "#000000"
		record["fields"] = [
				{
					"value": own_notes[idx].note
				}
		]
		record["footer"] = "<@" + own_notes[idx].author + ">"
		record["ts"] = own_notes[idx].timestamp
		#record["callback_id"] = "note_selection" + user_notes["hits"]["hits"][idx]["_id"]
		attachments.append(record)
		
	for idx in range(team_idx):
		record = {}

		print ("Team record " + str(idx))
		record["color"] = "#0079c0"
		record["fields"] = [
				{
					"value": team_notes[idx].note
				}
		]
		record["footer"] = "<@" + team_notes[idx].author + ">"
		record["ts"] = team_notes[idx].timestamp
		#record["callback_id"] = "note_selection" + team_notes["hits"]["hits"][idx]["_id"]
		attachments.append(record)
	
	if (team_idx == 0 and user_idx == 0):
		globals.slack_client.api_call("chat.postMessage", channel=channel, text="No notes found!", attachments=None)
	else:
		globals.slack_client.api_call("chat.postMessage", channel=channel, text="Here what I found:", attachments=attachments)
	
	return