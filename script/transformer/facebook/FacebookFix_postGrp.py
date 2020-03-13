#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import json
import re, os
import common as c

dirpath = os.getcwd()

def fct():
  path = dirpath+"/script/dataSource/facebook_data/groups" 
  all_msg = []

  try:
    with open(path+'/'+'your_posts_and_comments_in_groups.json') as f:
      data = json.load(f)


    #print(data['dmConversation'])
    for logData in data['group_posts']['activity_log_data']:
        ar_attach = []
        ar_data = []
        timestamp = logData['timestamp']
        title = logData['title']  


        if 'attachments' in logData:
            for attachments in logData['attachments']:
                ar_dt=[]
                for dt in attachments['data']:
                      uri = dt['media']['uri']   
                      creation_timestamp = dt['media']['creation_timestamp']
                      att_title = dt['media']['title']
                      clean_att_title = c.cleanText(att_title)
                      ar_dt.append({'uri':uri, 'creation_timestamp': creation_timestamp, 'title': clean_att_title})
                ar_attach.append(ar_dt)

        if 'data' in logData:
            for data2 in logData['data']:
                if 'update_timestamp' in data2:
                    update_timestamp = data2['update_timestamp']
                    ar_data.append({'update_timestamp': update_timestamp})

        clean_title = c.cleanText(title)
        


        my_msg = {  "timestamp": timestamp, 
                    "title": clean_title,

                    "attachments": ar_attach, 
                    "data": ar_data, 
                    }

        all_msg.append(my_msg)

    docsStr = ""
    for i in range(len(all_msg)-1):
        docsStr = docsStr + str(all_msg[i]) + "\n"
    docsStr = docsStr + str(all_msg[-1])

    docsStr = docsStr.replace("'",'"')


    docsStr.encode('ascii', errors='ignore').decode("utf-8")

    f = open(dirpath+"/script/dataSource/json-facebook_data/groups"+"/your_posts_and_comments_in_groups_fixed.json", "w")
    f.write(docsStr)
    f.close()
  except:
    print("Error in FB Fix postGrp")
