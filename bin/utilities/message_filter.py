# -*- coding: utf-8 -*-
"""
A module to store message filtering logic for the Hive Slack app 
"""

def is_direct_message(event_data):	# DM with a user
	return event_data['event']['channel'].startswith('D')
	
def is_public_message(event_data):	# Public channel message
	return event_data['event']['channel'].startswith('C')
	
def is_private_message(event_data):	# Private Channel or multi-person DM
	return event_data['event']['channel'].startswith('G')