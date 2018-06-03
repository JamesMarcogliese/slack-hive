# -*- coding: utf-8 -*-
"""
A module to store message filtering logic for the Hive Slack app 
"""

user_whitelist_enabled = False	# Default is False
user_whitelist = []
with open('./resources/user_whitelist.txt', 'r') as f:	# Load whitelist from resources
	user_whitelist = f.read().splitlines()
	
def use_whitelist(state):
	user_whitelist_enabled = state
	return

def is_app_home_event(event_data):		# From a message.app_home event
	return event_data.get("event").get("channel_type") == "app_home"
	
def is_bot_message(event_data):			# Message from a bot
	return event_data.get("event").get("bot_id") is not None
	
def is_changed_message(event_data):
	return event_data.get("event").get("subtype") == "message_changed"
	
def is_whitelisted_user(event_data):	# User in user_whitelist list	
	if (not user_whitelist_enabled):
		return True
	return event_data.get("event").get("user") in user_whitelist