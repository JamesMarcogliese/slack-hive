# -*- coding: utf-8 -*-
"""
A routing layer for the Hive Slack app 
"""
import json
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import os
from datetime import datetime
from elasticsearch import Elasticsearch
import requests
from pathlib import Path

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["BOT_TOKEN"]
CLIENT = SlackClient(SLACK_BOT_TOKEN)


@slack_events_adapter.on("message")
def handle_message(event_data):
	message = event_data["event"]
	
	#strippedText = message["text"].strip().lower()
	
	#if message["subtype"] is None and (strippedText == "help"):
	#	message = Path('help.txt').read_text()
	
	#if message.get("subtype") is None and strippedText.startsWith("set team"):
	#	message = "You have been added to the 
		
	if message.get("subtype") is None:
	
		doc = {
			'note': message["text"],
			'author': message["user"],
			'frequency': 0,
			'team': 'rollout',
			'timestamp': datetime.now()
			}
			
		res = es.index(index="note-index", doc_type='note', body=doc) 
		es.indices.refresh(index="note-index")
		
		channel = message["channel"]
		message = "Note saved!"
	
	CLIENT.api_call("chat.postMessage", channel=channel, text=message)
	

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)