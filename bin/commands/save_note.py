# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import sys
sys.path.append('../')
from utilities import globals
from datetime import datetime
from utilities import es_queries
import classes
import time

def pattern():
	return '^save (.*)'

def execute_event(event_data):
	print ("SaveNote")
	channel = event_data["event"]["channel"]
	
	#Search for author's team from author index
	author = es_queries.get_team(user)
		
	if (author is None):
		message = ("Wait! :raised_hand: I need to know what team you're on before I can save your notes!\n" 
				   "Please set your team by using the 'team' command!"
				   )
		globals.slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
		return 
	
	# Save note to note-index
	es_queries.save_note(event_data["event"]["text"].lstrip("save "), event_data["event"]["user"], author["hits"]["hits"][0]["_source"]["team"])

	globals.slack_client.api_call("chat.postMessage", channel=channel, text="Note saved!", attachments=None)
	return