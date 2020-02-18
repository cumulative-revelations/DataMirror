
#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

from elasticsearch import Elasticsearch, helpers 
import os, uuid, json
import common as c


# Generator to push bulk data from a JSON file into an Elasticsearch index / that function is changed according to files content
def bulkJsonData(json_file, _index,whatStuff):
	json_list = c.getDataFromFile(json_file)
	for doc in json_list:
		# use a 'yield' generator so that the data isn't loaded into memory
		if '{"index"' not in doc:

			json_doc = json.loads(doc)

			# clean the text in comments and title from special character and emojies after json conversion
			my_text = json_doc["First Name"]
			clean_my_text = c.cleanText(my_text)
			json_doc.update([ ("First Name", clean_my_text) ])	

			my_text2 = json_doc["Last Name"]
			clean_my_text2 = c.cleanText(my_text2)
			json_doc.update([ ("Last Name", clean_my_text2) ])	

			my_text3 = json_doc["Company"]
			clean_my_text3 = c.cleanText(my_text3)
			json_doc.update([ ("Company", clean_my_text3) ])	

			my_text4 = json_doc["Position"]
			clean_my_text4 = c.cleanText(my_text4)
			json_doc.update([ ("Position", clean_my_text4) ])	
		

			# add load_type, used later for filter
			json_doc.update([ ("load_type", whatStuff) ]) 
			json_doc.update([ ("source_type", "linkedIn") ])
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
		      "Connected On":   { "type":"date", "format":"dd MMM yyyy"},
		      "created_at": { "type": "alias", "path": "Connected On" }
		    } 
		  }
		}


	# Create index with a schema
	c.createIndex('dfp_people_li_connections', schema, elastic)


	inputFolder = "../dataSource/json-LinkedIn_data"
	for loadType in ["Connections"]:
		whatFile = os.path.join(inputFolder, loadType+'.json')
		#try:
		response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_people_li_connections",loadType))
		#except:
			#print ("Error in "+ whatFile)
			#pass


	print ("Insert LinkedIn Friends")

