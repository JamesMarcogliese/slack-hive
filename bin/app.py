# -*- coding: utf-8 -*-
"""
A routing layer for the Hive Slack app 
"""

from slackserver import SlackEventAdapter
from utilities import message_filter
from utilities import globals
import os

# Import command_dispatcher
import command_dispatcher

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack")

# Initialize globals object
globals.init()

# Responder to direct messages
@slack_events_adapter.on("message")
def handle_message(event_data):
	print ("\n -------- BEGINNING OF MESSAGE --------\n")
	print (event_data)
	print ("\n -------- END OF MESSAGE --------\n")
	if ((event_data.get("event").get("channel_type") == "app_home") and (event_data.get("event").get("bot_id") is None)):
		command_dispatcher.dispatch_event(event_data)

@slack_events_adapter.on("message_action")
def message_action(action_data):
	command_dispatcher.dispatch_action(action_data)

# Flask server with the default endpoint on port 3000
slack_events_adapter.start(host="0.0.0.0",port=3000)
