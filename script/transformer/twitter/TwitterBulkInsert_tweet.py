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

dirpath = os.getcwd()

# Generator to push bulk data from a JSON file into an Elasticsearch index / that function is changed according to files content
def bulkJsonData(json_file, _index,whatStuff):
  json_list = c.getDataFromFile(json_file)
  for doc in json_list:
    # use a 'yield' generator so that the data isn't loaded into memory
    if '{"index"' not in doc:

      json_doc = json.loads(doc)

      sentiment=[0,0,0]

      #print (doc)
      my_text = json_doc["full_text"]

      #get sentiment
      sentiment = s.getSentiment(my_text)

      clean_my_text = c.cleanText(my_text)
      json_doc.update([ ("full_text", clean_my_text) ])  


      my_text2 = json_doc["source"]
      clean_my_text2 = c.cleanText(my_text2)
      json_doc.update([ ("source", clean_my_text2) ])

      # Does not like "False", needed to be "false" !!!
      #my_text1 = json_doc["retweeted"]
      #clean_my_text1 = c.cleanText(str(my_text1))
      #json_doc.update([ ("retweeted", clean_my_text1) ]) 

      #if 'truncated' in json_doc:
      #  my_text3 = json_doc["truncated"]
      #  clean_my_text3 = c.cleanText(str(my_text3))
      #  json_doc.update([ ("truncated", clean_my_text3) ])

      #if 'favorited' in json_doc:
      #  my_text4 = json_doc["favorited"]
      #  clean_my_text4 = c.cleanText(str(my_text4))
      #  json_doc.update([ ("favorited", clean_my_text4) ])  


      #if 'possibly_sensitive' in json_doc:
      #  my_text5 = json_doc["possibly_sensitive"]
      #  clean_my_text5 = c.cleanText(str(my_text5))
      #  json_doc.update([ ("possibly_sensitive", clean_my_text5) ])  
       

    if 'in_reply_to_screen_name' in json_doc:
        my_name = json_doc["in_reply_to_screen_name"]
        clean_my_name = c.cleanText(my_name)
        json_doc.update([ ("in_reply_to_screen_name", clean_my_name) ]) 

    if 'user_mentions' in json_doc["entities"]:
      for usr in json_doc["entities"]['user_mentions']:
        my_name1 = usr["name"]
        clean_my_name1 = c.cleanText(my_name1)
        usr.update([ ("name", clean_my_name1) ]) 

        my_name2 = usr["screen_name"]
        clean_my_name2 = c.cleanText(my_name2)
        usr.update([ ("screen_name", clean_my_name2) ]) 

      for usr in json_doc["entities"]['urls']:
        my_name3 = usr["url"]
        clean_my_name3 = c.cleanText(my_name3)
        usr.update([ ("url", clean_my_name3) ]) 

        my_name4 = usr["expanded_url"]
        clean_my_name4 = c.cleanText(my_name4)
        usr.update([ ("expanded_url", clean_my_name4) ])

        my_name5 = usr["display_url"]
        clean_my_name5 = c.cleanText(my_name5)
        usr.update([ ("display_url", clean_my_name5) ]) 


    #if 'media' in json_doc:
    #  my_media = json_doc["media"]
    #  if 'additional_media_info' in my_media:
    #    my_name6 = my_media["additional_media_info"]
    #    clean_my_name6 = c.cleanText(my_name6)
    #    my_media.update([ ("additional_media_info", clean_my_name6) ]) 


      # add sentiment
      json_doc.update([ ("mySentiment", sentiment[0]) ]) 
      json_doc.update([ ("sentPositive", sentiment[1]) ]) 
      json_doc.update([ ("sentNegative", sentiment[2]) ]) 

      # add load_type, used later for filter
      json_doc.update([ ("load_type", whatStuff) ]) 
      json_doc.update([ ("source_type", "twitter") ]) 
      new_doc = str(json_doc).replace("'", '"')
      #print (new_doc)

      new_doc = new_doc.replace("False","false")
      new_doc = new_doc.replace("True","true")

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
        "created_at":{ "type":"date", "format":"EEE MMM dd HH:mm:ss ZZ yyyy"},
        "full_text":{ "type": "text", "analyzer": "my_english_analyzer", "fields": {"keyword": { "type": "keyword"}}, "fielddata": True},
        "all_text": { "type": "alias", "path": "full_text" }
        } 
      }


    }

  # Create index with a schema
  c.createIndex('dfp_text_tw_tweet', schema, elastic)


  inputFolder = dirpath+"/script/dataSource/json-twitter_data"
  for loadType in ["tweet"]:
    whatFile = os.path.join(inputFolder, loadType+'.json')
    try:
      response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_text_tw_tweet",loadType))
      print ("Insert Twitter Tweets")
    except:
      print ("Error in Twitter : "+ whatFile)
      pass

  


