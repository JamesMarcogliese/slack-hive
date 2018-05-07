# -*- coding: utf-8 -*-
"""
A module to store global objects for the Hive Slack app 
"""

from elasticsearch import Elasticsearch
from slackclient import SlackClient
import os

es = None
slack_client = None


def init():

	# Declare variables as module global
	global es
	global slack_client

	# Connect to Elasticsearch instance
	ELASTICSEARCH_ENDPOINT = os.environ["ELASTICSEARCH_ENDPOINT"]
	es = Elasticsearch([{'host': ELASTICSEARCH_ENDPOINT, 'port': 9200}])
	
	# Create a SlackClient for your bot to use for Web API requests
	SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
	slack_client = SlackClient(SLACK_BOT_TOKEN)
	
