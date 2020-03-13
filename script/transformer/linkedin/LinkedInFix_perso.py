#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import json, os
from ast import literal_eval
import common as c

dirpath = os.getcwd()

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
		mydict["source"] = 'linkedIn_profile'
		mydict["term"] = c.cleanText(str(item))
		mydict["key"] = c.cleanText(str(key))
		mylist.append(mydict)

	return mylist


def fct():
    path = dirpath+"/script/dataSource/json-LinkedIn_data" 
    print ("LinkedIn Perso - Fix")
    try:
        with open(path+'/'+'Profile.json') as json_file:
            data = json.load(json_file)
        #with open(path+'/'+'PhoneNumbers.json') as json_file1:
        #    data1 = json.load(json_file1)


        out = {}
        #out1 = {}

        out = flatten_json(data)
        #out1 = flatten(data1)


        #out.update(out1)
        theList = deflat(out)


        docsStr = ""
        for i in range(len(theList)-1):
        	docsStr = docsStr + str(theList[i]) + "\n"
        docsStr = docsStr + str(theList[-1])

        docsStr = docsStr.replace("'",'"')

        f = open(path+"/Profile_fixed.json", "w")
        f.write(docsStr)
        f.close()

    except:
        print("Error in LinkedIn Fix Perso")
        pass




