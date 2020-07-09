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
import shutil

dirpath = os.getcwd()

def find_parts(s_arr):
    strArr =  []
    pstack = []

    start=0
    end=0

    s='\n'.join(s_arr)
    s="{"+s+"}"

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
  count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and name.startswith("twitter-20")])

  if count == 0:
     print ("No Twitter Data")
  elif count > 1:
     print ("Duplicated Twitter File")
  else:
    # Get the file, unzip and fix it
    for r, d, f in os.walk(dirpath+"/script/dataSource"):
      for file in f:
        if file.endswith(".zip") and file.startswith("twitter-20"):

          inputFolderZipped = os.path.join(r,file)

          inputFolder = dirpath+'/script/dataSource/twitter_data'
          if not os.path.exists(inputFolder):
             os.mkdir(inputFolder)

          #with zipfile.ZipFile(inputFolderZipped, 'r') as zip_ref:
          #   zip_ref.extractall(inputFolder)

          print ("Twitter - Unzip")
          # Create a ZipFile Object and load sample.zip in it
          with ZipFile(inputFolderZipped, 'r') as zipObj:
             # Get a list of all archived file names from the zip
             listOfFileNames = zipObj.namelist()
             # Iterate over the file names
             for fileName in listOfFileNames:
                 # Check filename endswith csv
                 if fileName.endswith('.js'):
                     # Extract a single file from zip
                     zipObj.extract(fileName, inputFolder)
          

          #some people have the data in twitter/data file so we move it
          if os.path.exists(dirpath+'/script/dataSource/twitter_data/data'):
            source = dirpath+'/script/dataSource/twitter_data/data/'
            dest1 = dirpath+'/script/dataSource/twitter_data'
            thefiles = os.listdir(source)
            for f in thefiles:
              if f.endswith(".js"):
                if os.path.exists(dest1+"/"+f):
                  os.remove(dest1+"/"+f)
                shutil.move(source+f, dest1)




          print ("Twitter - Fix")
          jsonInputFolder = dirpath+'/script/dataSource/json-twitter_data'
          if not os.path.exists(jsonInputFolder):
            os.mkdir(jsonInputFolder)


          # root, d=directories, f = files
          for r, d, f in os.walk(inputFolder):
            #for c in f:
            for file in f:
              if file in ["tweet.js","like.js","follower.js","following.js","profile.js","phone-number.js"]: #file.endswith(".js"): #I can add a list of files
                  #subPath = os.path.join(r, file)
                  #print ("folder",r)
                  with codecs.open(os.path.join(r, file), 'r', encoding='utf8') as f_js:
                    MyFile=f_js.readlines()


                  MyFile_new=[]

                  try:
                    for i in range(len(MyFile)):
                      lines=MyFile[i].replace('\\n{ ','')
                      lines=lines.replace(' }…','')
                      lines=lines.replace(' }\\n','')

                      MyFile_new.append(lines)

                    #MyFile=open(os.path.join(r, file),encoding="utf8",'r').read()
                    docs = find_parts(MyFile_new[1:-1])
                    docsStr= '\n'.join(docs)
                    newFile = file.split('.')[0]+'.json'

                    r_parts = r.split("/")
                    m_parts = "/".join(r_parts[:-1])
                    with codecs.open(os.path.join(m_parts+"/json-"+r_parts[-1],newFile), 'w', encoding='utf8') as f_json:
                      f_json.write(docsStr)
                    f_json.close()
                  except:
                    pass







