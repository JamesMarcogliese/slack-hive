# -*- coding: utf-8 -*-
"""
A module to store Elasticsearch query logic for the Hive Slack app 

No function should return pure json.
"""
import sys
sys.path.append('../')
from classes.NoteRecord import NoteRecord
from classes.AuthorRecord import AuthorRecord
from utilities import globals
from datetime import datetime
import time
import json

def get_team(user):
	query = {
		"query": {
			"term": {
				"user": user
			}
		}
	}

	results = globals.es.search(index="author-index", body=query)
	
	if (results['hits']['total'] == 0):
		return None
	else:
		return AuthorRecord.fromjson(results["hits"]["hits"][0])
	
def delete_author_doc(doc_id):
	globals.es.delete(index="author-index", doc_type='author', id=doc_id)
	return
	
def delete_note_doc(doc_id):
	globals.es.delete(index="note-index", doc_type='note', id=doc_id)
	return


def add_author(user, selected_team):
	query = {
		"user": user,
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
					{"term": {"author" : user }}
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
					{"term": {"team": team }}
				],
				"must_not": [
					{"term": {"author": user }}
				]
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
		'team': team,
		'timestamp': unix_time
		}
	
	globals.es.index(index="note-index", doc_type="note", body=doc, refresh="true") 
	return
	
def indexes_exist():
	return globals.es.indices.exists(index="note-index") and globals.es.indices.exists(index="author-index")
	
def init_indexes():
	author_mapping_query = {
		"mappings" : {
			"author" : {
				"properties" : {
					"user" : { 
						"type" : "keyword" 
					},
					"team" : {
						"type" : "keyword"
					}
				}
			}
		}
	}
	
	note_mapping_query = {
		"mappings" : {
			"note" : {
				"properties" : {
					"author" : { 
						"type" : "keyword" 
					},
					"note" : {
						"type" : "text"
					},
					"team" : {
						"type" : "keyword"
					},
					"timestamp" : {
						"type" : "date"
					}
				}
			}
		}
	}
	globals.es.indices.create(index='author-index', body=author_mapping_query)
	globals.es.indices.create(index='note-index', body=note_mapping_query)
	#add_author("initial_user", "initial_team")
	#save_note("initial_note","initial_user","initial_team")
	return
	
def delete_indexes():
	globals.es.indices.delete(index='*')
	return