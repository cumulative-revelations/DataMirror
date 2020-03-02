#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import json, os, sys, codecs, csv, ast



def fct():
    path = '../../dataSource' 

    new_data = [{"id": 1,"name": "User", "source" : "No Source"}]


    try:

        # Education LinkedIn
        if os.path.isfile(path+'/LinkedIn_data/Education.csv'):
            with codecs.open(path+'/LinkedIn_data/Education.csv', 'r', encoding='utf8') as f_csv:
                reader = csv.DictReader(f_csv)
                rows = list(reader)

                json_data = json.dumps(list(rows))
                json_arr = ast.literal_eval(json_data)

                new_data.append({"id": "Edu","parent" : "root", "name": "Education", "source" : "LinkedIn"})

                for i in range(len(json_arr)):
                    new_data.append({"id": "Edu"+str(i), "parent": "Edu", "name": json_arr[i]["Degree Name"], "source": "LinkedIn"})
                    new_data.append({"id": "EduSch"+str(i), "parent": "Edu"+str(i), "name": json_arr[i]["School Name"], "source": "LinkedIn"})
                    new_data.append({"id": "EduStr"+str(i), "parent": "Edu"+str(i), "name": json_arr[i]["Start Date"], "source": "LinkedIn"})
                    new_data.append({"id": "EduEnd"+str(i), "parent": "Edu"+str(i), "name": json_arr[i]["End Date"], "source": "LinkedIn"})


        # Positions LinkedIn
        if os.path.isfile(path+'/LinkedIn_data/Positions.csv'):
            with codecs.open(path+'/LinkedIn_data/Positions.csv', 'r', encoding='utf8') as f_csv:
                reader = csv.DictReader(f_csv)
                rows = list(reader)

                json_data = json.dumps(list(rows))
                json_arr = ast.literal_eval(json_data)

                new_data.append({"id": "Pos","parent" : "root", "name": "Positions", "source" : "LinkedIn"})

                for i in range(len(json_arr)):
                    new_data.append({"id": "Pos"+str(i), "parent": "Pos", "name": json_arr[i]["Title"], "source": "LinkedIn"})
                    new_data.append({"id": "EduComp"+str(i), "parent": "Pos"+str(i), "name": json_arr[i]["Company Name"], "source": "LinkedIn"})
                    new_data.append({"id": "EduLoc"+str(i), "parent": "Pos"+str(i), "name": json_arr[i]["Location"], "source": "LinkedIn"})
                    new_data.append({"id": "EduStrO"+str(i), "parent": "Pos"+str(i), "name": json_arr[i]["Started On"], "source": "LinkedIn"})
                    new_data.append({"id": "EduEndO"+str(i), "parent": "Pos"+str(i), "name": json_arr[i]["Finished On"], "source": "LinkedIn"})

     
        # Skills LinkedIn
        if os.path.isfile(path+'/LinkedIn_data/Skills.csv'):
            with codecs.open(path+'/LinkedIn_data/Skills.csv', 'r', encoding='utf8') as f_csv:
                reader = csv.DictReader(f_csv)
                rows = list(reader)

                json_data = json.dumps(list(rows))
                json_arr = ast.literal_eval(json_data)

                new_data.append({"id": "Skill","parent" : "root", "name": "Skills", "source" : "LinkedIn"})

                for i in range(len(json_arr)):
                    new_data.append({"id": "Skill"+str(i), "parent": "Skill", "name": json_arr[i]["Name"], "source": "LinkedIn"})


        # create the file
        with open('../../vegaStuff/Qualifications.json', 'w') as outfile:
            json.dump(new_data, outfile)
            print ("Create Qualification Vega")

    except:
       print ("Error in Qualification Vega")
       pass
