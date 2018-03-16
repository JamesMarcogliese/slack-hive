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
	user = event_data['event']['user'] 
	channel = event_data["event"]["channel"]	

	#Search for author's team from author index
	query = {
			"query": {
				"match": {
					"author": user
				}
			}
		}
	if (globals.es.indices.exists(index="author-index")):
		author = globals.es.search(index="author-index", body=query)
	
	if (author['hits']['total'] == 0) or not(globals.es.indices.exists(index="author-index")):
		message = ("Wait! :raised_hand:I need to know what team you're on before I can search for notes!\n" 
				   "Please set your team by using the 'team' command!"
				   )
		globals.slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
		return 
		
	user_query_own = {
		"query": {
			"bool": {
				"should": [
					{"match": { "note": message }}
				],
				"must": {
					"match": { "author": user }
				},
				"minimum_should_match": "100%"
			}
		}
	}
	
	user_query_team = {
		"query": {
			"bool": {
				"should": [
					{"match": { "note": message }}
				],
				"must": {
					"match": { "team": author["hits"]["hits"][0]["_source"]["team"] }
				},
				"must_not": {
					"match": { "author": user }
				},
				"minimum_should_match": "100%"
			}
		}
	}
	
	if (globals.es.indices.exists(index="note-index")):
		user_notes = globals.es.search(index="note-index", body=user_query_own)
		team_notes = globals.es.search(index="note-index", body=user_query_team)
	else:
		print ("Note-Index not found!")
		
		
	#-------------------------------------------------------------	
	
	
	
	attachments = [] # --------------------------------------------------------------------------
	
	if (int(user_notes["hits"]["total"]) >= 4):
		user_idx = 4
	elif (int(user_notes["hits"]["total"]) == 0):
		user_idx = 0
	else:
		user_idx = int(user_notes["hits"]["total"])
		
	if (int(team_notes["hits"]["total"]) >= 4):
		team_idx = 4
	elif (int(team_notes["hits"]["total"]) == 0):
		team_idx = 0
	else:
		team_idx = int(team_notes["hits"]["total"])
		
	for idx in range(user_idx):
		record = {}

		print ("User record " + str(idx))
		record["color"] = "#000000"
		record["fields"] = [
				{
					"value": user_notes["hits"]["hits"][idx]["_source"]["note"]
				}
		]
		record["footer"] = user_notes["hits"]["hits"][idx]["_source"]["author"]
		record["ts"] = user_notes["hits"]["hits"][idx]["_source"]["timestamp"]
		#record["callback_id"] = "note_selection" + user_notes["hits"]["hits"][idx]["_id"]
		attachments.append(record)
		
	for idx in range(team_idx):
		record = {}

		print ("Team record " + str(idx))
		record["color"] = "#0079c0"
		record["fields"] = [
				{
					"value": team_notes["hits"]["hits"][idx]["_source"]["note"]
				}
		]
		record["footer"] = team_notes["hits"]["hits"][idx]["_source"]["author"]
		record["ts"] = team_notes["hits"]["hits"][idx]["_source"]["timestamp"]
		#record["callback_id"] = "note_selection" + team_notes["hits"]["hits"][idx]["_id"]
		attachments.append(record)
	
	globals.slack_client.api_call("chat.postMessage", channel=channel, text="Here what I found:", attachments=attachments)
	
	print ("review")
	

	
	