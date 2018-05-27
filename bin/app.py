# -*- coding: utf-8 -*-
"""
A routing layer for the Hive Slack app 
"""

from slackserver import SlackEventAdapter
from utilities import message_filter
from utilities import es_queries
from utilities import globals
import command_dispatcher
import logging
import os

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Enable/Disable whitelist
message_filter.use_whitelist(True)

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack")

# Initialize globals object
globals.init()

# Initialize elasticsearch indexes, if empty
if (not es_queries.indexes_exist()):
	es_queries.init_indexes()

# Responder to direct messages
@slack_events_adapter.on("message")
def handle_message(event_data):
	logger.info('Incoming event...')
	logger.debug(event_data)
	if (message_filter.is_app_home_event(event_data)
	  and not message_filter.is_bot_message(event_data) 		  
	  and message_filter.is_whitelisted_user(event_data)):
		command_dispatcher.dispatch_event(event_data)

@slack_events_adapter.on("message_action")
def message_action(action_data):
	command_dispatcher.dispatch_action(action_data)

# Flask server with the default endpoint on port 3000
slack_events_adapter.start(host="0.0.0.0",port=3000)
