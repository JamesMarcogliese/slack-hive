# -*- coding: utf-8 -*-
"""
A routing layer for the Hive Slack app 
"""
from slackserver import SlackEventAdapter
from elasticsearch import Elasticsearch
from slackclient import SlackClient
import os

# Import commands module
import commands

# Connect to Elasticsearch instance
commands.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack")

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
commands.slack_client = SlackClient(SLACK_BOT_TOKEN)

# Responder to direct messages
@slack_events_adapter.on("message")
def handle_message(event_data):
	if event_data.get("event").get("subtype") is None: 
		commands.command_invoker(event_data)
		
@slack_events_adapter.on("message_action")
def message_action(action_data):
	commands.action_invoker(action_data)

# Flask server with the default endpoint on port 3000
slack_events_adapter.start(port=3000)