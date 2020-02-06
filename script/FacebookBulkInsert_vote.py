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
		for attachments in json_doc['attachments']:
			for dt in attachments['data']:
				for pl in dt['poll']['options']:
						my_text = pl["option"]
						clean_my_text = c.cleanText(my_text)
						pl.update([ ("option", clean_my_text) ])	

						my_vote = str(pl["voted"])
						clean_my_vote = c.cleanText(my_vote)
						pl.update([ ("voted", clean_my_vote) ])	

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
	  "mappings":{
	     "properties":{                                     
		      "timestamp":   { "type":"date", "format":"date_optional_time||epoch_second"},
		      "created_at": { "type": "alias", "path": "timestamp" }
	    	}
	  	}

	}

	# Create index with a schema
	c.createIndex('dfp_fb_vote', schema, elastic)

	inputFolder = "dataSource/json-facebook_data/other_activity"
	for loadType in ["polls_you_voted_on"]:
		whatFile = os.path.join(inputFolder, loadType+'.json')
		try:
			response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_fb_vote",loadType))
		except:
			print ("Error in "+ whatFile)
			pass


	print ("Insert Facebook Votes")

