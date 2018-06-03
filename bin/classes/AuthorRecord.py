# -*- coding: utf-8 -*-
"""

"""

class AuthorRecord(object):
	author = None
	team = None
	doc_id = None

	def __init__(self, doc_id, author, team):
		self.doc_id = doc_id
		self.author = author
		self.team = team
		
	@classmethod	
	def fromjson(cls, jsondata):
		doc_id = jsondata["_id"]
		author = jsondata["_source"]["user"]
		team = jsondata["_source"]["team"]
		return cls(doc_id, author, team)