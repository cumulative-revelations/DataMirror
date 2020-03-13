#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import json, os, ast, twint, codecs, csv, sys
from ast import literal_eval
sys.path.insert(0, '..')
import common as c

dirpath = os.getcwd()

def facebookTags(path):

    json_file = open(path+'json-facebook_data/posts/your_posts_1.json', encoding="utf8", errors='ignore')
    json_list = [line.strip() for line in json_file]

    list_tags=[]
    for doc in json_list:
        json_doc = json.loads(doc)

        if 'tags' in json_doc:
            for usr in json_doc["tags"]:
                name = usr
                list_tags.append(name)
    return list_tags



def twitterTags(path):

    json_file = open(path+'json-twitter_data/tweet.json', encoding="utf8", errors='ignore')
    json_list = [line.strip() for line in json_file]

    list_tags=[]
    for doc in json_list:
        json_doc = json.loads(doc)
        
        if not json_doc['full_text'].startswith("RT @"):
            for usr in json_doc["entities"]['user_mentions']:
                name = usr["name"]
                screen_name = usr["screen_name"]
                list_tags.append({"name":name, "screen_name":screen_name})
    return list_tags



def usersFollowers(MyUsername,path):
    list_arr =[]
    c = twint.Config()
    c.Username = MyUsername
    c.Store_csv = True
    c.Hide_output = True

    c.Output = path+"followers.csv"
    twint.run.Followers(c)

    # open file in read mode
    followers_arr=[]
    with open(path+"followers.csv", 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            followers_arr.append(row[0])

    return followers_arr



def usersFollowings(MyUsername,path):
    list_arr =[]
    c = twint.Config()
    c.Username = MyUsername
    c.Store_csv = True
    c.Hide_output = True
    c.Output = path+"followings.csv"
    twint.run.Followers(c)

    # open file in read mode
    followings_arr=[]
    with open(path+"followings.csv", 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            followings_arr.append(row[0])

    return followings_arr


def fct():
    path = dirpath+'/script/dataSource/' 
    new_data = []
    try:

        #  LinkedIn friends

        json_file = open(path+'json-LinkedIn_data/Connections.json', encoding="utf8", errors='ignore')
        json_list = [line.strip() for line in json_file]

        for doc in json_list:
            json_doc = json.loads(doc)
            new_data.append({"name": c.cleanText(json_doc["First Name"] + ' ' + json_doc["Last Name"]) ,"screen_name" : c.cleanText(json_doc["First Name"] + ' ' + json_doc["Last Name"]), "tags": 1, "type": "friend", "source" : "LinkedIn"})
           

        #  Twitter friends

        # remove files if existed
        file_folr = open(path+'followers.csv',"w") 
        file_folg = open(path+'followings.csv',"w") 


        if os.path.isfile(path+'json-twitter_data/account.json'):
            with open(path+'json-twitter_data/account.json') as json_file:
                data = json.load(json_file)

            user_name = data["account"]["username"]
            list_tags = twitterTags(path)
            #print (list_tags)


            # get lists of followers
            list_followers = usersFollowers(user_name,path)
            list_followings = usersFollowings(user_name,path)

            #print (list_followers)
            for fr in range(len(list_followers)):
                count = 1
                theName = list_followers[fr]
                theType = "follower"

                for tag in range(len(list_tags)):
                    #print(list_followers[fr], list_tags[tag]["screen_name"])
                    if list_followers[fr].lower() == list_tags[tag]["screen_name"].lower():
                        count = count + 1
                        theName = list_tags[tag]["name"]

                for fg in range(len(list_followings)):
                    if list_followers[fr].lower() == list_followings[fg].lower():
                        count = count + 1
                        theType = "follower/following" 


                new_data.append({"name": c.cleanText(theName) ,"screen_name" : c.cleanText(list_followers[fr]), "tags": count, "type": theType, "source" : "Twitter"})



            # add the those I follow and they dont follow me
            for fg in range(len(list_followings)):
                if list_followings[fg] not in list_followers:
                    count = 1
                    theName = list_followings[fg]
                    theType = "following"

                    for tag in range(len(list_tags)):
                        if list_followings[fg].lower() == list_tags[tag]["screen_name"].lower():
                            count = count + 1
                            theName = list_tags[tag]["name"]


                new_data.append({"name": c.cleanText(theName) ,"screen_name" : c.cleanText(list_followings[fg]), "tags": count, "type": theType, "source" : "Twitter"})


        #  Facebook friends

        # get lists of tags
        list_ftags = facebookTags(path)
        list_friends=[]

        json_file = open(path+'json-facebook_data/friends/friends.json', encoding="utf8", errors='ignore')
        json_list = [line.strip() for line in json_file]

        for doc in json_list:
            json_doc = json.loads(doc)

            list_friends.append(json_doc['name'])

        for fr in range(len(list_friends)):
            count = 1

            for ftag in range(len(list_ftags)):
                if list_friends[fr].lower() == list_ftags[ftag].lower():
                    count = count + 1


            new_data.append({"name": c.cleanText(list_friends[fr]) ,"screen_name" : c.cleanText(list_friends[fr]), "tags": count, "type": "friend", "source" : "Facebook"})


        # create the file
        #with open('../../vegaStuff/friends.json', 'w') as outfile:
        #    json.dump(new_data, outfile)
        #    print ("Create Friends")

        string = ""
        for mydata in new_data[:-1]:
            string = string + str(mydata) + "\n"
        string = string + str(new_data[-1])

        string = string.replace("'",'"')


        file_res = open(dirpath+'/vegaFiles/friends.json',"w") 
        file_res.write(string)
        file_res.close()
        print ("Collect Friends")

    except:
       print ("Error in Collect Friends")
       pass





