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
		if '{"index"' not in doc:

			json_doc = json.loads(doc)

			# clean the text in comments and title from special character and emojies after json conversion
			if loadType == 'pages':
				my_text = json_doc["name"]
				clean_my_text = c.cleanText(my_text)
				json_doc.update([ ("name", clean_my_text) ])
			else:
				my_text = json_doc["title"]
				clean_my_text = c.cleanText(my_text)
				json_doc.update([ ("title", clean_my_text) ])				

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
		  "mappings":{
		    "properties":{   
		      "timestamp":   { "type":"date", "format":"date_optional_time||epoch_second"},
		      "created_at": { "type": "alias", "path": "timestamp" }
		    } 
		  }
		}

	# Create index with a schema
	c.createIndex('dfp_fb_likes', schema, elastic)


	inputFolder = "../dataSource/json-facebook_data/likes_and_reactions"
	for loadType in ["likes_on_external_sites","pages","posts_and_comments"]:
		whatFile = os.path.join(inputFolder, loadType+'.json')

		try:
			response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_fb_likes",loadType))
			print ("Insert Facebook Friends")
		except:
			print ("Error in Facebook :"+ whatFile)
		pass


	

