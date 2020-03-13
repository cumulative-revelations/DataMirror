#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

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

      if whatStuff == "Email Addresses":
        my_text = json_doc["Email Address"]
        json_doc.update([ ("term", my_text) ]) 
        json_doc.update([ ("key", "email") ]) 

      if whatStuff == "PhoneNumbers":
        my_text2 = json_doc["Number"]
        json_doc.update([ ("term", my_text2) ]) 
        json_doc.update([ ("key", "phone") ]) 

      if whatStuff == "Profile_fixed":      
        my_text = json_doc["term"]
        clean_my_text = c.cleanText(my_text)
        json_doc.update([ ("term", clean_my_text) ])  

        my_text2 = json_doc["key"]
        clean_my_text2 = c.cleanText(my_text2)
        json_doc.update([ ("key", clean_my_text2) ])

      # add load_type, used later for filter
      json_doc.update([ ("load_type", whatStuff) ]) 
      json_doc.update([ ("source_type", "linkedIn") ]) 
      new_doc = str(json_doc).replace("'", '"')

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
              "source": { "type":"text"},
              "term":   { "type":"text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True},                           
              "key":   { "type":"text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True}
              } 
          }
    }

  # Create index with a schema
  c.createIndex('dfp_perso_li', schema, elastic)


  inputFolder = dirpath+"/script/dataSource/json-LinkedIn_data"
  for loadType in ["Profile_fixed","PhoneNumbers","Email Addresses"]:
    whatFile = os.path.join(inputFolder, loadType+'.json')
    try:
      response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_perso_li",loadType))
      print ("Insert LinkedIn Personal Data")
    except:
      print ("Error in Insert LinkedIn : "+ whatFile)
      pass

  
