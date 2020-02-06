#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

from elasticsearch import Elasticsearch, helpers 
import os, uuid, json
import common as c


# Generator to push bulk data from a JSON file into an Elasticsearch index / that function is changed according to files content
def bulkJsonData(json_file, _index,loadType):
	json_list = c.getDataFromFile(json_file)
	for doc in json_list:
		# use a 'yield' generator so that the data isn't loaded into memory
		if '{"index"' not in doc and '"sender_name":' in doc:

			json_doc = json.loads(doc)

			# clean the text in comments and title from special character and emojies after json conversion
			my_name = json_doc["sender_name"]
			clean_my_name = c.cleanText(my_name)
			json_doc.update([ ("sender_name", clean_my_name) ])	

			if 'content' in json_doc:
				my_text = json_doc["content"]
				clean_my_text = c.cleanText(my_text)
				json_doc.update([ ("content", clean_my_text) ])

			if 'reactions' in json_doc:
				for react in json_doc["reactions"]:
					my_react = react["reaction"]
					clean_my_react = c.cleanText(my_react)
					react.update([ ("reaction", clean_my_react) ])

			# add load_type, used later for filter
			json_doc.update([ ("load_type", loadType) ]) 
			json_doc.update([ ("source_type", "facebook") ])
			new_doc = str(json_doc).replace("'", '"')
			#print (new_doc)

			yield {
				"_index": _index,
				"_id": uuid.uuid4(),
				 "_source": new_doc
			}


def fct():
	elastic = Elasticsearch(hosts=[{'host':'localhost','port':9200}])

	# the Schema, used to force specific types and to add alias/ it is changed according to files content
	schema = {    

		  "settings": {
		     "analysis": {
		       "analyzer": {
		         "my_english_analyzer": {"type": "standard","stopwords": "_english_"}
		       }
		     }
		   },

		  "mappings":{
		    "properties":{   
		      "timestamp_ms":   { "type":"date", "format":"date_optional_time||epoch_millis"},
		      "created_at": { "type": "alias", "path": "timestamp_ms" },
		      "content":{ "type": "text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True},
		      "all_text": { "type": "alias", "path": "content" }
		    } 
		  }
		}

	# Create index with a schema
	c.createIndex('dfp_fb_messages', schema, elastic)


	inputFolder = "json-facebook_data/messages"
	for r, d, f in os.walk(inputFolder):
		for file in f:
			if file.endswith(".json"):
				whatToDo = file

				loadType = r.split("/")[2]
				whatFile = os.path.join(r, whatToDo)
				try:
					response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_fb_messages",loadType))
				except:
					print ("Error in "+ whatFile)
				pass


	print ("Insert Facebook Messages")
