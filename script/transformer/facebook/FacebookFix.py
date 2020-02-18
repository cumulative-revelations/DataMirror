#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import os
import sys
import codecs
from zipfile import ZipFile

def find_parts(s_arr):
    strArr =  []
    pstack = []

    start=0
    end=0

    s='\n'.join(s_arr)
    #s="{"+s+"}"

    for i, c in enumerate(s):
        if '{' in c :
            pstack.append(i)

        elif '}' in c :

            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            elif len(pstack) == 1:
                start = pstack.pop()
                end = i+1
                myStr = s[start:end].replace('\n','')
                strArr.append(myStr)
            else:
                pstack.pop()
          
    if len(pstack) > 0:
      raise IndexError("No matching opening parens at: " + str(pstack.pop()))
    
    return strArr

def fct():
  # Duplicated or no files?
  count = len([name for name in os.listdir('../dataSource') if name.endswith(".zip") and name.startswith("facebook-")])
  if count == 0:
     print ("No Facebook Data")
  elif count > 1:
     print ("Duplicated Facebook File")

  # Get the file, unzip and fix it
  for r, d, f in os.walk("../dataSource"):
    for file in f:
      if file.endswith(".zip") and file.startswith("facebook-"):

        inputFolderZipped = os.path.join(r,file)

        inputFolder = '../dataSource/facebook_data'
        if not os.path.exists(inputFolder):
        	os.mkdir(inputFolder)

        #with zipfile.ZipFile(inputFolderZipped, 'r') as zip_ref:
        #	zip_ref.extractall(inputFolder)

        print ("Facebook - Unzip ")

        # Create a ZipFile Object and load sample.zip in it
        with ZipFile(inputFolderZipped, 'r') as zipObj:
           # Get a list of all archived file names from the zip
           listOfFileNames = zipObj.namelist()
           # Iterate over the file names
           for fileName in listOfFileNames:
               # Check filename endswith csv
               if fileName.endswith('.json'):
                   # Extract a single file from zip
                   zipObj.extract(fileName, inputFolder)




        print ("Facebook - Fix")
        jsonInputFolder = '../dataSource/json-facebook_data'
        if not os.path.exists(jsonInputFolder):
        	os.mkdir(jsonInputFolder)



        for r, d, f in os.walk(inputFolder):
          r_parts = r.split('/')
          if not os.path.exists(r_parts[0]+"/"+r_parts[1]+'/json-'+'/'.join(r_parts[2:])):
            os.mkdir(r_parts[0]+"/"+r_parts[1]+'/json-'+'/'.join(r_parts[2:]))



        # r=root, d=directories, f=files
        for r, d, f in os.walk(inputFolder):
            for file in f:
              if file.endswith(".json"): #I can add a list of files
                #subPath = os.path.join(r, file)
                #print ("file: ", file)

                if file.endswith("_fixed.json"):
                  pass
                else:  
                  with codecs.open(os.path.join(r, file), 'r', encoding='utf8') as f_js:
                    #print (os.path.join(r, file))
                    MyFile=f_js.readlines()


                  #MyFile=open(os.path.join(r, file),encoding="utf8",'r').read()
                  docs = find_parts(MyFile[1:-1])
                  docsStr= '\n'.join(docs)
                  newFile = file.split('.')[0]+'.json'
                  r_parts = r.split('/')
                  #print (r_parts[0]+'/json-'+'/'.join(r_parts[1:])+'/'+newFile)

                  with codecs.open(os.path.join(r_parts[0]+"/"+r_parts[1]+'/json-'+'/'.join(r_parts[2:]),newFile), 'w', encoding='utf8') as f_json:
                    f_json.write(docsStr)
                  f_json.close()
                

