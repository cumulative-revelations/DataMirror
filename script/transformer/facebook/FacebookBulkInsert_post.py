#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

from elasticsearch import Elasticsearch, helpers 
import os, uuid, json
import common as c
import sentiment as s

# Generator to push bulk data from a JSON file into an Elasticsearch index / that function is changed according to files content
def bulkJsonData(json_file, _index, whatStuff):
	json_list = c.getDataFromFile(json_file)
	for doc in json_list:

		json_doc = json.loads(doc)

		sentiment=[0,0,0]
		
	    # use a 'yield' generator so that the data isn't loaded into memory
		if '{"index"' not in doc:

			# clean the text in comments and title from special character and emojies after json conversion
			if 'data' in json_doc:
				for dt in json_doc['data']:
					if 'post' in dt:
						my_text = dt["post"]

						#get sentiment
						sentiment = s.getSentiment(my_text)

						clean_my_text = c.cleanText(my_text)
						dt.update([ ("post", clean_my_text) ])
						json_doc.update([ ("all_text", clean_my_text) ])	

			if 'attachments' in json_doc:
				for att in json_doc['attachments']:
					if 'data' in att:
						for dt in att['data']:
							if 'external_context' in dt:
								if 'name' in dt["external_context"]:
									my_text2 = dt["external_context"]["name"]
									clean_my_text2 = c.cleanText(my_text2)
									dt["external_context"].update([ ("name", clean_my_text2) ])	 

							if 'media' in dt:
								my_title2 = dt['media']['title']
								clean_my_title2 = c.cleanText(my_title2)
								dt['media'].update([ ("title", clean_my_title2) ])	 

								if 'description' in dt['media']:
									my_description = dt['media']["description"]
									clean_my_description = c.cleanText(my_description)
									dt['media'].update([ ("description", clean_my_description) ])

							if 'place' in dt:
								my_loc = dt["place"]["coordinate"]
								my_lat = my_loc["latitude"]
								my_lon = my_loc["longitude"]
								new_my_loc = [my_lon,my_lat]
								dt["place"].update([ ("location", new_my_loc) ])	 	 
	           		

			if 'title' in json_doc:
				my_title = json_doc["title"]
				clean_my_title = c.cleanText(my_title)
				json_doc.update([ ("title", clean_my_title) ])	

			# add sentiment
			json_doc.update([ ("mySentiment", sentiment[0]) ]) 
			json_doc.update([ ("sentPositive", sentiment[1]) ]) 
			json_doc.update([ ("sentNegative", sentiment[2]) ]) 

			# add load_type, used later for filter
			json_doc.update([ ("load_type", whatStuff) ]) 
			json_doc.update([ ("source_type", "facebook") ])
			new_doc = str(json_doc).replace("'", '"')


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
		      		"post": { "type": "text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True}
		      	}
		      },
		      "attachments": {
		      	"properties": {
			      "data": {
			      	"properties": {
				      "place": {
				      	"properties": {
				      		"location": {"type": "geo_point"}
				      	}		      	
			      	}
			      }
			     }
			     
		      	}
		      }        
	    	}
	  	}

	}

	# Create index with a schema
	c.createIndex('dfp_text_fb_posts', schema, elastic)


	inputFolder = "../dataSource/json-facebook_data/posts"
	for loadType in ["your_posts_1"]:
		whatFile = os.path.join(inputFolder, loadType+'.json')
		try:
			response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_text_fb_posts",loadType))
			print ("Insert Facebook Posts")
		except:
			print ("Error in Facebook Posts")
			pass






	#