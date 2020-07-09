#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""
import sys, os

dirpath = os.getcwd()



sys.path.insert(0, 'script/transformer/generic')
import Profile_vega
import Qualification_vega
import FriendsCollecting
import FriendBulkInsert
import TopicDetection
import TopicBulkInsert
import SentimentCollecting
import SentimentBulkInsert



#LinkedIn
count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and "_LinkedInDataExport_" in name])
if count == 0:
 print ("No LinkedIn Data")
elif count > 1:
 print ("Duplicated LinkedIn File")
else:

	sys.path.insert(0, 'script/transformer/linkedin')
	import LinkedInFix
	import LinkedInBulkInsert_connections
	#import LinkedInBulkInsert_perso
	#import LinkedInBulkInsert_qualification
	import LinkedInFix_perso




#Facebook
count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and name.startswith("facebook-")])
if count == 0:
 print ("No Facebook Data")
elif count > 1:
 print ("Duplicated Facebook File")
else:

	sys.path.insert(0, 'script/transformer/facebook')
	import FacebookFix	
	import FacebookFix_perso		
	import FacebookFix_postGrp
	import FacebookBulkInsert_comment	
	import FacebookBulkInsert_follow	
	import FacebookBulkInsert_friend	
	import FacebookBulkInsert_like	
	#import FacebookBulkInsert_perso	
	import FacebookBulkInsert_post
	import FacebookBulkInsert_postGrp
	import FacebookBulkInsert_vote



#Twitter
count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and name.startswith("twitter-20")])
if count == 0:
 print ("No Twitter Data")
elif count > 1:
 print ("Duplicated Twitter File")
else:

	sys.path.insert(0, 'script/transformer/twitter')
	import TwitterFix
	import TwitterFix_perso
	import TwitterBulkInsert_follow
	import TwitterBulkInsert_like
	#import TwitterBulkInsert_perso
	import TwitterBulkInsert_tweet








if __name__ == '__main__':


	#LinkedIn
	count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and "_LinkedInDataExport_" in name])
	if count == 0:
	 print ("No LinkedIn Data")
	elif count > 1:
	 print ("Duplicated LinkedIn File")
	else:

		LinkedInFix.fct()
		LinkedInFix_perso.fct()
		LinkedInBulkInsert_connections.fct()
		#LinkedInBulkInsert_perso.fct()



	#Facebook
	count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and name.startswith("facebook-")])
	if count == 0:
	 print ("No Facebook Data")
	elif count > 1:
	 print ("Duplicated Facebook File")
	else:

		FacebookFix.fct()
		FacebookFix_perso.fct()
		FacebookFix_postGrp.fct()
		FacebookBulkInsert_comment.fct()
		FacebookBulkInsert_follow.fct()
		FacebookBulkInsert_friend.fct()
		FacebookBulkInsert_like.fct()
		#FacebookBulkInsert_perso.fct()
		FacebookBulkInsert_post.fct()
		FacebookBulkInsert_postGrp.fct()
		FacebookBulkInsert_vote.fct()




	#Twitter
	count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and name.startswith("twitter-20")])
	if count == 0:
	 print ("No Twitter Data")
	elif count > 1:
	 print ("Duplicated Twitter File")
	else:

		TwitterFix.fct()
		TwitterFix_perso.fct()
		TwitterBulkInsert_follow.fct()
		TwitterBulkInsert_like.fct()
		#TwitterBulkInsert_perso.fct()
		TwitterBulkInsert_tweet.fct()




	Profile_vega.fct()
	Qualification_vega.fct()
	FriendsCollecting.fct()
	FriendBulkInsert.fct()
	TopicDetection.fct()
	TopicBulkInsert.fct()
	SentimentCollecting.fct()
	SentimentBulkInsert.fct()

