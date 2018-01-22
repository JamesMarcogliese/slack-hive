# -*- coding: utf-8 -*-
"""
A module for handling commands for the Hive Slack app 
"""
from datetime import datetime
from pathlib import Path
import requests
import json
import re

es = None
slack_client = None

def save_note(event_data):
	print ("SaveNote")
	channel = event_data["event"]["channel"]
	
	#Search for author's team from author index
	query = {
			"query": {
				"term": {
					"author": event_data['event']['user'] 
				}
			}
		}
	if (es.indices.exists(index="author-index")):
		author = es.search(index="author-index", body=query)
	
	if (author['hits']['total'] == 0) or not(es.indices.exists(index="author-index")):
		message = ("Wait! :raised_hand:I need to know what team you're on before I can save your notes!\n" 
				   "Please set your team by using the 'team' command!"
				   )
		slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
		return 
	
	# Save note to note-index
	doc = {
		'note': event_data["event"]["text"].lstrip("save "),
		'author': event_data["event"]["user"],
		'frequency': 0,
		'team': author["hits"]["hits"][0]["_source"]["team"],
		'timestamp': datetime.now()
		}
	
	es.index(index="note-index", doc_type="note", body=doc, refresh="true") 

	slack_client.api_call("chat.postMessage", channel=channel, text="Note saved! :notebook:", attachments=None)
	return

def find_note(event_data):
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
	if (es.indices.exists(index="author-index")):
		author = es.search(index="author-index", body=query)
	
	if (author['hits']['total'] == 0) or not(es.indices.exists(index="author-index")):
		message = ("Wait! :raised_hand:I need to know what team you're on before I can save your notes!\n" 
				   "Please set your team by using the 'team' command!"
				   )
		slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
		return 
	
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
	
	notes = es.search(index="author-index", body=query)
	
#	query = {
#		"query": {
#			"query_string": {
#				"query": message
#			}
#		}
#	}

def set_team(event_data):
	print ("setTeam")
	
	if event_data["type"] == 'event_callback':
		# Send the list to the user
		teams_menu = json.load(open('teams_menu.json'))
		channel = event_data["event"]["channel"]
		slack_client.api_call("chat.postMessage", channel=channel, text="What team do you belong to?", attachments=teams_menu)
		return
	elif event_data["type"] == 'interactive_message':
		# Check the users selection
		user = event_data["user"]["id"]
		selected_team = event_data["actions"][0]["selected_options"][0]["value"]
		channel = event_data["channel"]["id"]
		
	#Search for author's team from author index
	query = {
			"query": {
				"term": {
					"author": user 
				}
			}
		}
	if (es.indices.exists(index="author-index")):
		author = es.search(index="author-index", body=query)	
		if (author['hits']['total'] != 0):
			es.delete(index="author-index", doc_type='author', id=author['hits']['hits'][0]['_id'])
	
	doc = {
		'author': user,
		'team': selected_team
		}
	
	es.index(index="author-index", doc_type='author', body=doc, refresh="true") 
	
	message = "You now share notes with the " + selected_team + " team!"
	slack_client.api_call("chat.update", channel=channel, ts=event_data["message_ts"], text=message, attachments=None)
	return

def review_notes(event_data):

	if event_data["type"] == 'interactive_message': 
		print (event_data)
		id = event_data["callback_id"].lstrip("note_selection")
		es.delete(index="note-index", doc_type='note', id=id)
		
		channel = event_data["channel"]["id"]
		message = "Note `" + event_data["original_message"]["attachments"][int(event_data["attachment_id"])-1]["text"] + "` has been deleted!"
		slack_client.api_call("chat.update", channel=channel, ts=event_data["message_ts"], text=message, attachments=None)
		return
	
	channel = event_data["event"]["channel"]	
	query = {
			"sort" : [
				{ "timestamp": {"order": "desc"}} 
			],
			"query": {
				"term": {
					"author": event_data['event']['user'] 
				}
			}
		}
	
	notes = es.search(index="note-index", body=query)
	
	if notes["hits"]["total"] == 0:
		slack_client.api_call("chat.postMessage", channel=channel, text="You haven't saved any notes yet!")
		return
		
	attachments = []
	
	for idx in range(notes["hits"]["total"]):
		record = {}
		print ("record " + str(idx))
		record["text"] = notes["hits"]["hits"][idx]["_source"]["note"]
		record["fallback"] = "Please upgrade slack to see this message!"
		record["actions"] = [
				{
					"name": "option",
					"text": "Delete",
					"type": "button",
					"value": "delete"
				}   
			]
		record["callback_id"] = "note_selection" + notes["hits"]["hits"][idx]["_id"]
		attachments.append(record)
	
	slack_client.api_call("chat.postMessage", channel=channel, text="Here are your notes:", attachments=attachments)
	
	print ("review")
	
def help(event_data):
	print ("help")
	channel = event_data["event"]["channel"]
	help_menu = Path('help_menu.txt').read_text()
	slack_client.api_call("chat.postMessage", channel=channel, text=help_menu, attachments=None)
	return
	
def fallback(event_data):
	channel = event_data["event"]["channel"]
	print ("fallback")
	message = ":confounded: Sorry, I don't understand. Type 'help' to see a list of what I can do!"
	slack_client.api_call("chat.postMessage", channel=channel, text=message, attachments=None)
	return 

def command_invoker(event_data):
	patterns=['^save (.*)', '^find (.*)', '^team', '^help', '^review', '.*']
	functions=['save_note', 'find_note', 'set_team', 'help', 'review_notes', 'fallback']
	message_text = event_data["event"]['text']
	for idx, pattern in enumerate(patterns):
		if re.compile(patterns[idx]).search(message_text) is not None:
			return eval(functions[idx])(event_data)
			
def action_invoker(action_data):
	callback_types=['team_selection', "note_selection"]
	functions=['set_team', 'review_notes']
	for idx, callback_type in enumerate(callback_types):
		if action_data["callback_id"].startswith(callback_types[idx]):
			return eval(functions[idx])(action_data)