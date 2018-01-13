# -*- coding: utf-8 -*-
"""
A routing layer for the Hive Slack app 
"""
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import os

# Import commands module
import commands

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask webserver for incoming traffic from Slack
#app = Flask(__name__)

# Responder to direct messages
@slack_events_adapter.on("message")
def handle_message(event_data):
	message = event_data["event"]
	
	if message.get("subtype") is None: 
		channel = message["channel"]
		message,attachment = commands.identify_command(event_data)
		slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=attachment)
		
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
	# Parse the request payload
	message_action = json.loads(request.form["payload"])
	message,attachment = commands.set_team(message)
	slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=attachment)
	

# Flask server with the default endpoint on port 3000
slack_events_adapter.start(port=3000)