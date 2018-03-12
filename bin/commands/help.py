# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

from pathlib import Path
import sys
sys.path.append('../')
from utilities import globals

def pattern():
	return '^help'
	
def execute_event(event_data):
	print ("help")
	channel = event_data["event"]["channel"]
	help_menu = Path('./resources/help_menu.txt').read_text()
	globals.slack_client.api_call("chat.postMessage", channel=channel, text=help_menu, attachments=None)
	return