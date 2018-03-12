# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import sys
sys.path.append('../')
from utilities import globals

def pattern():
	return '^review'
	
def execute_event(event_data):

	if event_data["type"] == 'interactive_message': 
		print (event_data)
		id = event_data["callback_id"].lstrip("note_selection")
		globals.es.delete(index="note-index", doc_type='note', id=id)
		
		channel = event_data["channel"]["id"]
		message = "Note `" + event_data["original_message"]["attachments"][int(event_data["attachment_id"])-1]["text"] + "` has been deleted!"
		globals.slack_client.api_call("chat.update", channel=channel, ts=event_data["message_ts"], text=message, attachments=[])
		return
	
	channel = event_data["event"]["channel"]	
	query = {
			"sort" : [
				{ "timestamp": {"order": "desc"}} 
			],
			"query": {
				"match": {
					"author": event_data['event']['user'] 
				}
			}
		}
	
	if (globals.es.indices.exists(index="note-index")):
		notes = globals.es.search(index="note-index", body=query)
	
	if notes["hits"]["total"] == 0:
		globals.slack_client.api_call("chat.postMessage", channel=channel, text="You haven't saved any notes yet!")
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
		record["ts"] = notes["hits"]["hits"][idx]["_source"]["timestamp"]
		record["callback_id"] = "note_selection" + notes["hits"]["hits"][idx]["_id"]
		attachments.append(record)
	
	globals.slack_client.api_call("chat.postMessage", channel=channel, text="Here are your notes:", attachments=attachments)
	
	print ("review")