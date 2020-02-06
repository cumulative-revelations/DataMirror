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
def bulkJsonData(json_file, _index, whatStuff):
	json_list = c.getDataFromFile(json_file)
	for doc in json_list:

		json_doc = json.loads(doc)

		# clean the text in comments and title from special character and emojies after json conversion
		if "data" in json_doc:
			my_text_location = json_doc["data"][0]["comment"]
			my_text = my_text_location["comment"]
			clean_my_text = c.cleanText(my_text)
			my_text_location.update([ ("comment", clean_my_text) ])	
			json_doc.update([ ("all_text", clean_my_text) ])

			if "group" in my_text_location:
				my_group = my_text_location["group"]
				clean_my_group = c.cleanText(my_group)
				my_text_location.update([ ("group", clean_my_group) ])	

		my_title = json_doc["title"]
		clean_my_title = c.cleanText(my_title)
		json_doc.update([ ("title", clean_my_title) ])	


		# add load_type, used later for filter
		json_doc.update([ ("load_type", whatStuff) ]) 
		json_doc.update([ ("source_type", "facebook") ]) 
		new_doc = str(json_doc).replace("'", '"')


	    # use a 'yield' generator so that the data isn't loaded into memory
		if '{"index"' not in new_doc:
			yield {
				"_index": _index,
				"_id": uuid.uuid4(),
				 "_source": new_doc
			}

def fct():
	# create a new instance of the Elasticsearch client class 
	#elastic = Elasticsearch("localhost") 
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
	                          
		      "timestamp":   { "type":"date", "format":"date_optional_time||epoch_second"},
		      "created_at": { "type": "alias", "path": "timestamp" },
		      "all_text": { "type": "text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True},
		      
		      "data":  {
	          	"properties": {
		      		"comment":{ 
				      	"type": "nested", 
			          	"properties": {
				      		"comment":{ "type": "text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True}
				      		}
		      			}
		      		}
		      	}

	    	}
	  	}

	}

	# Create index with a schema
	c.createIndex('dfp_text_fb_comment', schema, elastic)

	inputFolder = "dataSource/json-facebook_data/comments"
	for loadType in ["comments"]:
		whatFile = os.path.join(inputFolder, loadType+'.json')
		try:
			response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_text_fb_comment",loadType))
		except:
			print ("Error in "+ whatFile)
			pass

	print ("Insert Facebook Comments")
