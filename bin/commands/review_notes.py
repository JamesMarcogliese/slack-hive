# -*- coding: utf-8 -*-
"""
A command module for the Hive Slack app 
"""

import sys
sys.path.append('../')
from utilities import globals
from utilities import es_queries
import classes

def pattern():
	return '^review'
	
def execute_event(event_data):

	if event_data["type"] == 'interactive_message': 
		print (event_data)
		id = event_data["callback_id"] #.lstrip("note_selection")
		print ("ID TO BE DELETED: " + id)
		globals.es.delete(index="note-index", doc_type='note', id=id[14:])
		
		channel = event_data["channel"]["id"]
		message = "Note `" + event_data["original_message"]["attachments"][int(event_data["attachment_id"])-1]["text"] + "` has been deleted!"
		globals.slack_client.api_call("chat.update", channel=channel, ts=event_data["message_ts"], text=message, attachments=[])
		return
	
	channel = event_data["event"]["channel"]	
	
	notes = es_queries.get_all_user_notes(event_data['event']['user'])
	
	if (len(notes) == 0):
		globals.slack_client.api_call("chat.postMessage", channel=channel, text="You haven't saved any notes yet!")
		return
		
	attachments = []
	
	if (len(notes) >= 10): # I'm only displaying the first 10 for demo, will need pageation for prod
		total = 10
	elif (len(notes) == 0):
		total = 0
	else:
		total = len(notes)
	
	for idx in range(total):
		record = {}
		print ("record " + str(idx))
		record["text"] = notes[idx].note
		record["fallback"] = "Please upgrade slack to see this message!"
		record["actions"] = [
				{
					"name": "option",
					"text": "Delete",
					"type": "button",
					"value": "delete"
				}   
			]
		record["ts"] = notes[idx].timestamp
		record["callback_id"] = "note_selection" + notes[idx].doc_id
		print ("IDS: " + notes[idx].doc_id)
		attachments.append(record)
	
	globals.slack_client.api_call("chat.postMessage", channel=channel, text="Here are your notes:", attachments=attachments)
	
	print ("review")