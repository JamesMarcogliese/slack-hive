# -*- coding: utf-8 -*-
"""
A module to store Elasticsearch query logic for the Hive Slack app 

No function should return pure json.
"""

sys.path.append('../')
from classes import NoteRecord
from utilities import globals
from datetime import datetime
import time
import json

def get_team(author):
	query = {
		"query": {
			"term": {
				"field": "author",
					"value": author
			}
		}
	}

	author = globals.es.search(index="author-index", body=query)
	
	if (author['hits']['total'] == 0):
		return None
	else:
		return author["hits"]["hits"][0]["_source"]["team"]
	
def delete_author_doc(doc_id):
	globals.es.delete(index="author-index", doc_type='author', id=doc_id)
	return
	
def delete_note_doc(doc_id):
	globals.es.delete(index="note-index", doc_type='note', id=doc_id)
	return


def add_author(user, selected_team):
	query = {
		"author": user,
		"team": selected_team
		}
	
	globals.es.index(index="author-index", doc_type='author', body=query, refresh="true") 
	return
		
def search_user_notes(user, keywords):
	query = {
		"query": {
			"bool": {
				"must": [
					{"common": { "note": {"query": keywords }}},
					{"term": {"field": "author", "value": user}}
				]
			}
		}
	}
	
	response = globals.es.search(index="note-index", body=query)
	notes = []
	for element in response['hits']['hits']:
		notes.append(NoteRecord.fromjson(element))

	return notes
	
def search_team_notes(user, team, keywords):
	query = {
		"query": {
			"bool": {
				"must": [
					{"common": { "note": {"query": keywords }}},
					{"term": {"field": "team", "value": team}}
				],
				"must_not": {
					{"term": {"field": "user", "value": user}}
				}
			}
		}
	}
	
	response = globals.es.search(index="note-index", body=query)
	notes = []
	for element in response['hits']['hits']:
		notes.append(NoteRecord.fromjson(element))

	return notes

def get_all_user_notes(user):
	query = {
		"sort" : [
			{ "timestamp": {"order": "desc"}} 
		],
		"query": {
			"match": {
				"author": user 
			}
		}
	}
	
	response = globals.es.search(index="note-index", body=query)
	
	notes = []
	for element in response['hits']['hits']:
		notes.append(NoteRecord.fromjson(element))

	return notes

def save_note(note, author, team):
	dt = datetime.now()
	unix_time = time.mktime(dt.timetuple())
	
	doc = {
		'note': note,
		'author': author,
		'frequency': 0,
		'team': team,
		'timestamp': unix_time
		}
	
	globals.es.index(index="note-index", doc_type="note", body=doc, refresh="true") 
	return
	
def indexes_exist():
	return globals.es.indices.exists(index="note-index") 
		and globals.es.indices.exists(index="author-index")
	
def init_indexes():
	add_author("initial_user", "initial_team")
	save_note("initial_note","initial_user","initial_team")
	return