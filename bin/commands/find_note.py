# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import sys
sys.path.append('../')
from utilities import globals

def pattern():
	return '^find (.*)'

def execute_event(event_data):
	print ("findNote")
	message = event_data['event']['text'].lstrip('find ')
	
#	query = {
#		"query": {
#			"query_string" : { 
#				"query" : message 
#			},
#			"term": {
#				"team": 
#			}
#		}
#	}

	#Search for author's team from author index
	query = {
			"query": {
				"term": {
					"author": event_data['event']['user'] 
				}
			}
		}
	if (globals.es.indices.exists(index="author-index")):
		author = es.search(index="author-index", body=query)
	
	if (author['hits']['total'] == 0) or not(globals.es.indices.exists(index="author-index")):
		message = ("Wait! :raised_hand:I need to know what team you're on before I can search for notes!\n" 
				   "Please set your team by using the 'team' command!"
				   )
		globals.slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
		return 
		
	userQuery = {
	
	}
	
	userQuery = {
	
	}
	
	https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-common-terms-query.html
	
	https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html
	query = {
		"query": {
			"filtered": {
				"query": {
					"query_string" : { 
						"query" : message 
					}
				},
				"filter": {
					"or": [
						{
							"term" : {
								"author" : event_data["event"]["user"]
							},
						},
						{
							"term": {
								"team": author["hits"]["hits"][0]["_source"]["team"]
							}
						}
					]
				}
			}
		}
	}
	
	notes = globals.es.search(index="author-index", body=query)
	
#	query = {
#		"query": {
#			"query_string": {
#				"query": message
#			}
#		}
#	}