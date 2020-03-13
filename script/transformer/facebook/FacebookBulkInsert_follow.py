#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

from elasticsearch import Elasticsearch, helpers 
import os, uuid, json
import common as c

dirpath = os.getcwd()

# Generator to push bulk data from a JSON file into an Elasticsearch index / that function is changed according to files content
def bulkJsonData(json_file, _index,whatStuff):
	json_list = c.getDataFromFile(json_file)
	for doc in json_list:
		# use a 'yield' generator so that the data isn't loaded into memory
		if '{"index"' not in doc:

			json_doc = json.loads(doc)

			# clean the text in comments and title from special character and emojies after json conversion
			my_text = json_doc["name"]
			clean_my_text = c.cleanText(my_text)
			json_doc.update([ ("name", clean_my_text) ])	

			# add load_type, used later for filter
			json_doc.update([ ("load_type", whatStuff) ]) 
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
		  "mappings":{
		    "properties":{   
		      "name":  { "type":"keyword" },
		      "timestamp":   { "type":"date", "format":"date_optional_time||epoch_second"},
		      "created_at": { "type": "alias", "path": "timestamp" }
		    } 
		  }
		}

	# Create index with a schema
	c.createIndex('dfp_people_fb_follow', schema, elastic)


	inputFolder = dirpath+"/script/dataSource/json-facebook_data/following_and_followers"
	for loadType in ["followers","following"]:
		whatFile = os.path.join(inputFolder, loadType+'.json')
		try:
			response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_people_fb_follow",loadType))
			print ("Insert Facebook "+ loadType)
		except:
			print ("Error in Facebook : "+ whatFile)
			pass


	
