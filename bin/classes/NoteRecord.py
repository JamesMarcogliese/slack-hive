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
		cls.note = jsondata["_source"]["note"]
		cls.author = jsondata["_source"]["author"]
		cls.team = jsondata["_source"]["team"]
		cls.timestamp = jsondata["_source"]["timestamp"]
		cls.doc_id = jsondata["_id"]
		return cls