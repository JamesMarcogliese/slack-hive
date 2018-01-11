# -*- coding: utf-8 -*-
"""
A routing layer for the Hive Slack app 
"""
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import os

import commands

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["BOT_TOKEN"]
CLIENT = SlackClient(SLACK_BOT_TOKEN)

# Responder to direct messages
@slack_events_adapter.on("message")
def handle_message(event_data):
	message = event_data["event"]
	
	if message.get("subtype") is None: 
		channel = message["channel"]
		message = commands.identifyCommand(event_data)
		CLIENT.api_call("chat.postMessage", channel=channel, text=message)
	
	
	

	


# Example reaction emoji echo
#@slack_events_adapter.on("reaction_added")
#def reaction_added(event_data):
#    event = event_data["event"]
#    emoji = event["reaction"]
#    channel = event["item"]["channel"]
#    text = ":%s:" % emoji
#    CLIENT.api_call("chat.postMessage", channel=channel, text=text)

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)