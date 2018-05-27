# -*- coding: utf-8 -*-
"""

"""

class AuthorRecord(object):
	author = None
	team = None
	doc_id = None

	def __init__(self, doc_id, author, team):
		self.doc_id = note
		self.author = author
		self.team = team
		
	@classmethod	
	def fromjson(cls, jsondata):
		cls.author = jsondata["_source"]["author"]
		cls.team = jsondata["_source"]["team"]
		cls.doc_id = jsondata["_id"]
		return cls