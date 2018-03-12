# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import sys
sys.path.append('../')
from utilities import globals

def pattern():
	return '.*'
	
def execute_event(event_data):
	channel = event_data["event"]["channel"]
	print ("fallback")
	message = "Sorry, I don't understand. Type 'help' to see a list of what I can do!"
	globals.slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
	return 