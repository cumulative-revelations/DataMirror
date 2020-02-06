#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
""" 

import os
import sys
import codecs
import json
import common as c


def find_parts(s):
    strArr =  []
    pstack = []

    start=0
    end=0

    
    for i, c in enumerate(s):
        if '{' in c :
            pstack.append(i)

        elif '}' in c :

            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            elif len(pstack) == 1:
                start = pstack.pop()
                end = i+1
                myStr = s[start:end]#.replace('\n','')
                strArr.append(myStr)
            else:
                pstack.pop()
          
    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))
    
    return strArr

def fct():
    inputFile = 'dataSource/twitter_data/direct-message.js'
    outputFile = 'dataSource/json-twitter_data/direct-message_fixed.json'

    try:
        with codecs.open(os.path.join(inputFile), 'r', encoding='utf8') as f_js:
        				MyFile=f_js.read()

        #MyFile=open(os.path.join(r, file),encoding="utf8",'r').read()
        docs = find_parts(MyFile[1:-1])
        docsStr= '\n'.join(docs)



        ##########
        data = json.loads(docsStr)
        all_msg = []

        conv = data['dmConversation']
        convId = conv['conversationId']
        for msg in conv['messages']:
            theMsg = msg['messageCreate']

            msg_id = theMsg['id']   
            msg_recipientId = theMsg['recipientId']
            msg_senderId = theMsg['senderId']
            msg_txt = theMsg['text']         
            msg_createdAt = theMsg['createdAt']   
            msg_mediaUrls = theMsg['mediaUrls']   

            clean_msg_txt = c.cleanText(msg_txt)

            my_msg = {  "conversationId": convId, 
                        "msgId": msg_id, 
                        "recipientId": msg_recipientId, 
                        "senderId": msg_senderId, 
                        "text": clean_msg_txt,
                        "createdAt":msg_createdAt, 
                        "mediaUrls":msg_mediaUrls
                        }

            all_msg.append(my_msg)

        docsStr = ""
        for i in range(len(all_msg)-1):
            docsStr = docsStr + str(all_msg[i]) + "\n"
        docsStr = docsStr + str(all_msg[-1])

        docsStr = docsStr.replace("'",'"')


        docsStr.encode('ascii', errors='ignore').decode("utf-8")

        f = open(outputFile, "w", encoding='utf8')
        f.write(docsStr)
        f.close()
        
    except:
        print("Error in Tw Fix Msg")





