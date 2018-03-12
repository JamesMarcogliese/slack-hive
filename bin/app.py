# -*- coding: utf-8 -*-
"""
A routing layer for the Hive Slack app 
"""

from slackserver import SlackEventAdapter
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
	if event_data.get("event").get("subtype") is None: 
		command_dispatcher.dispatch_event(event_data)
		
@slack_events_adapter.on("message_action")
def message_action(action_data):
	command_dispatcher.dispatch_action(action_data)

# Flask server with the default endpoint on port 3000
slack_events_adapter.start(port=3000)