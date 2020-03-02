#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import json, os, ast
from ast import literal_eval


def fct():
    path = '../../dataSource/' 

    new_data = [{"id": 1,"name": "User", "source" : "No Source"}]


    try:

        #  LinkedIn Profile
        if os.path.isfile(path+'json-LinkedIn_data/Profile.json'):
            data=""
            linkedin_parent = 2
            new_data.append({"id": linkedin_parent,"parent" : 1, "name": "LinkedIn", "source" : "No Source"})
            with open(path+'json-LinkedIn_data/Profile.json') as json_file:
                data = json.load(json_file)

            i=3
            for n in ['First Name','Last Name','Maiden Name','Address','Zip Code','Geo Location','Birth Date','Industry','Twitter Handles','Websites','Instant Messengers']:
                if data[n] != '' :
                    new_data.append({"id": i,"parent" : linkedin_parent, "name": n+": "+data[n], "source" : "Linkedin"})
                    i=i+1



        #  Twitter Profile
        if os.path.isfile(path+'json-twitter_data/profile.json'):
            data=""
            twitter_parent = i
            new_data.append({"id": twitter_parent,"parent" : 1, "name": "Twitter", "source" : "No Source"})
            with open(path+'json-twitter_data/profile.json') as json_file:
                data = json.load(json_file)

            i=i+1
            tw_p = data["profile"]

            if "description" in tw_p:
                if "bio" in tw_p["description"]:
                    new_data.append({"id": i,"parent" : twitter_parent, "name": "bio: "+tw_p["description"]["bio"], "source" : "Twitter"})
                    i=i+1
                if "website" in tw_p["description"]:
                    new_data.append({"id": i,"parent" : twitter_parent, "name": "website: "+tw_p["description"]["website"], "source" : "Twitter"})
                    i=i+1
                if "location" in tw_p["description"]:
                    new_data.append({"id": i,"parent" : twitter_parent, "name": "location: "+tw_p["description"]["location"], "source" : "Twitter"})
                    i=i+1     


        #  Facebook Profile
        if os.path.isfile(path+'json-facebook_data/profile_information/profile_information.json'):
            data=""
            facebook_parent = i
            new_data.append({"id": facebook_parent,"parent" : 1, "name": "Facebook", "source" : "No Source"})
            with open(path+'json-facebook_data/profile_information/profile_information.json') as json_file:
                data = json.load(json_file)

            i=i+1
            if data["name"]["full_name"] != "" :
                new_data.append({"id": i,"parent" : facebook_parent, "name": "full_name: "+data["name"]["full_name"], "source" : "Facebook"})
                i=i+1
            if data["name"]["first_name"] != "" : 
                new_data.append({"id": i,"parent" : facebook_parent, "name": "first_name: "+data["name"]["first_name"], "source" : "Facebook"})
                i=i+1
            if data["name"]["middle_name"] != "" : 
                new_data.append({"id": i,"parent" : facebook_parent, "name": "middle_name: "+data["name"]["middle_name"], "source" : "Facebook"})
                i=i+1   
            if data["name"]["last_name"] != "" :
                new_data.append({"id": i,"parent" : facebook_parent, "name": "last_name: "+data["name"]["last_name"], "source" : "Facebook"})
                i=i+1 


            if data["birthday"]["year"] != "" : 
                new_data.append({"id": i,"parent" : facebook_parent, "name": "birthday -year: "+str(data["birthday"]["year"]), "source" : "Facebook"})
                i=i+1
            if data["birthday"]["month"] != "" : 
                new_data.append({"id": i,"parent" : facebook_parent, "name": "birthday -month: "+str(data["birthday"]["month"]), "source" : "Facebook"})
                i=i+1   
            if data["birthday"]["day"] != "" :
                new_data.append({"id": i,"parent" : facebook_parent, "name": "birthday -day: "+str(data["birthday"]["day"]), "source" : "Facebook"})
                i=i+1 

            if data["gender"]["gender_option"] != "" :
                new_data.append({"id": i,"parent" : facebook_parent, "name": "gender: "+data["gender"]["gender_option"], "source" : "Facebook"})
                i=i+1 


        # create the file
        with open('../../vegaStuff/Profile.json', 'w') as outfile:
            json.dump(new_data, outfile)
            print ("Create Profile Vega")

    except:
       print ("Error in Profile Vega")
       pass


