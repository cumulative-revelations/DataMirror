#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

from elasticsearch import Elasticsearch, helpers, sys
import os, uuid, json
sys.path.insert(0, '..')
import common as c

dirpath = os.getcwd()

# Generator to push bulk data from a JSON file into an Elasticsearch index / that function is changed according to files content
def bulkJsonData(json_file, _index,whatStuff):

    json_file1 = open(json_file, encoding="utf8", errors='ignore')
    json_list = [line.strip() for line in json_file1]

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
          "mappings":{
            "properties":{   
              "date": { "type":"date", "format":"EEE MMM dd HH:mm:ss ZZ yyyy||date_optional_time||epoch_second"},
              "mySentiment": { "type":"float"},
              "sentPositive": { "type":"float"},
              "sentNegative": { "type":"float"},

            } 
          }
        }

    # Create index with a schema
    c.createIndex('dfp_sentiment', schema, elastic)


    inputFolder = dirpath+'/vegaFiles/'

    for r, d, f in os.walk(inputFolder):
        for file in f:
            if file.endswith("sentiment.json"):
                whatFile = os.path.join(inputFolder, file)
                try:
                    file_part=file.split(".")[0]
                    response = helpers.bulk(elastic, bulkJsonData(whatFile, "dfp_sentiment",file_part))
                    print ("Insert Sentiment")
                except:
                    print ("Error in Insert Sentiment")
                    pass



