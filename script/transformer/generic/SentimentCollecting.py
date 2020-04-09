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


def getSentiment(path):

    new_data=[]

    # facebook post
    json_file = open(path+'json-facebook_data/posts/your_posts_1.json', encoding="utf8", errors='ignore')
    json_list = [line.strip() for line in json_file]

    for doc in json_list:
        json_doc = json.loads(doc)

        if 'all_text' in json_doc:
            my_text = json_doc["all_text"]
            my_time = json_doc["timestamp"]
            sentiment = s.getSentiment(my_text)

            new_data.append({"date": my_time , "mySentiment": sentiment[0] ,"sentPositive" : sentiment[1], "sentNegative": sentiment[2], "type": "post", "source" : "facebook"})


    # facebook post group
    json_file1 = open(path+'json-facebook_data/groups/your_posts_and_comments_in_groups_fixed.json', encoding="utf8", errors='ignore')
    json_list1 = [line.strip() for line in json_file1]

    for doc in json_list1:
        json_doc = json.loads(doc)
        
        my_time = json_doc["timestamp"]

        if 'data' in json_doc:
          for dt in json_doc['data']:
            if 'post' in dt:
              my_text = dt["post"]
              sentiment = s.getSentiment(my_text)

              new_data.append({"date": my_time , "mySentiment": sentiment[0] ,"sentPositive" : sentiment[1], "sentNegative": sentiment[2], "type": "postGroup", "source" : "facebook"})



    # facebook comments
    json_file2 = open(path+'json-facebook_data/comments/comments.json', encoding="utf8", errors='ignore')
    json_list2 = [line.strip() for line in json_file2]

    for doc in json_list2:
        json_doc = json.loads(doc)
        my_time = json_doc["timestamp"]

        if "data" in json_doc:
            my_text_location = json_doc["data"][0]["comment"]
            my_text = my_text_location["comment"]
            
            sentiment = s.getSentiment(my_text)

            new_data.append({"date": my_time , "mySentiment": sentiment[0] ,"sentPositive" : sentiment[1], "sentNegative": sentiment[2], "type": "comment", "source" : "facebook"})



    # twitter
    json_file3 = open(path+'json-twitter_data/tweet.json', encoding="utf8", errors='ignore')
    json_list3 = [line.strip() for line in json_file3]

    for doc in json_list3:
        json_doc = json.loads(doc)

        if not json_doc['full_text'].startswith("RT @"):
            my_text = json_doc["full_text"]
            my_time = json_doc["created_at"]
            sentiment = s.getSentiment(my_text)

            new_data.append({"date": my_time , "mySentiment": sentiment[0] ,"sentPositive" : sentiment[1], "sentNegative": sentiment[2], "type": "tweet", "source" : "twitter"})


    return new_data




def fct():

    #try:  
    path = dirpath+'/script/dataSource/' 
    new_data=getSentiment(path) 

    string = ""
    for mydata in new_data[:-1]:
      string = string + str(mydata) + "\n"
    string = string + str(new_data[-1])

    string = string.replace("'",'"')

    file_res = open(dirpath+'/vegaFiles/sentiment.json',"w") 
    file_res.write(string)
    file_res.close()
    print ("Collect Sentiment")
    #except:
    #   print ("Error in Collect Sentiment")
    #   pass
