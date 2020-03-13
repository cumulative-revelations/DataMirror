#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import os, uuid, sys
import common as c


# clean text
def cleanText(inputString):
    outputString = inputString.encode('ascii', 'ignore').decode('ascii')  #remove emojy
    outputString = outputString.replace("'"," ").replace('"'," ").replace("\n","").lower() #remove ' and " since they cause issues at some point
    return outputString



# Create index with a schema
def createIndex(indexName, schemaName, elasticName):
    # Delete index if exists
	if elasticName.indices.exists(indexName):
  		elasticName.indices.delete(index=indexName, ignore=[400, 404])

	elasticName.indices.create(index=indexName, ignore=400, body=schemaName) 


# A simple function that gets the working path of the Python script and returns it
def scriptPath():
	path = os.path.dirname(os.path.realpath(__file__))
	if os.name == 'posix': # posix is for macOS or Linux
		path = path + "/"
	else:
		path = path + chr(92) # backslash is for Windows
	return path


# This function opens a file and returns its contents as a list of strings split by linebreaks
def getDataFromFile(myFile, path=scriptPath()):
	file = open(str(myFile), encoding="utf8", errors='ignore')
	data = [line.strip() for line in file]
	file.close()
	return data



'''
Notes:
# "timestamp":   { "type":"date", "format":"date_optional_time||epoch_millis"}
# created at is of format : Mon Jul 08 21:03:53 +0000 2019

"timestamp":   { "type":"date", "format":"date_optional_time||epoch_second"},

'''