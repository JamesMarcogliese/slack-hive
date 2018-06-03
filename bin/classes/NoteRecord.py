# -*- coding: utf-8 -*-
"""

"""

class NoteRecord(object):
	note = None
	author = None
	team = None
	timestamp = None
	doc_id = None

	def __init__(self, note, author, team, timestamp, doc_id):
		self.note = note
		self.author = author
		self.team = team
		self.timestamp = timestamp
		self.doc_id = doc_id
		
	@classmethod	
	def fromjson(cls, jsondata):
		note = jsondata["_source"]["note"]
		author = jsondata["_source"]["author"]
		team = jsondata["_source"]["team"]
		timestamp = jsondata["_source"]["timestamp"]
		doc_id = jsondata["_id"]
		return cls(note,author,team,timestamp,doc_id)