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
						yield {
								"_index": _index,
								"_id": uuid.uuid4(),
									"_source": doc
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
							"source": { "type":"text" , "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True},
							"term":   { "type":"text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True},                           
							"key":   { "type":"text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True}
							} 
					}
			}

	# Create index with a schema
	c.createIndex('dfp_perso_tw', schema, elastic)


	inputFolder = dirpath+"/script/dataSource/json-twitter_data"
	for loadType in ["personal_data_fixed"]:
			whatFile = os.path.join(inputFolder, loadType+'.json')
			try:
				response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_perso_tw",loadType))
				print ("Insert Twitter Personal Data")
			except:
					print ("Error in Twitter : "+ whatFile)
					pass

	
