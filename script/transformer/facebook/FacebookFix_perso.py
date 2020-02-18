#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import json, os
from ast import literal_eval
import common as c

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def deflat(a_dict):
    mylist = []
    for key, item in a_dict.items():
        mydict={}
        mydict["source"] = 'facebook_profile'
        myItem = c.cleanText(str(item))
        myKey = c.cleanText(str(key))
        mydict["term"] = str(myItem)
        mydict["key"] = str(myKey)
        mylist.append(mydict)
    return mylist


def fct():
    path = "../dataSource/json-facebook_data/profile_information" 
    print ("Facebook Perso - Fix")
    try:
        with open(path+'/'+'profile_information.json') as json_file:
            data = json.load(json_file)


        out = {}
        out = flatten_json(data)

        theList = deflat(out)


        docsStr = ""
        for i in range(len(theList)-1):
        	docsStr = docsStr + str(theList[i]) + "\n"
        docsStr = docsStr + str(theList[-1])

        docsStr = docsStr.replace("'",'"')

        f = open(path+"/profile_information_fixed.json", "w")
        f.write(docsStr)
        f.close()
        
    except:
        print("Error in FB Fix Perso")
        pass




