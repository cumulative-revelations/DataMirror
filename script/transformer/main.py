#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

import sys

sys.path.insert(0, 'script/transformer/twitter')
import TwitterFix
import TwitterFix_perso
import TwitterBulkInsert_follow
import TwitterBulkInsert_like
#import TwitterBulkInsert_perso
import TwitterBulkInsert_tweet

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

sys.path.insert(0, 'script/transformer/linkedin')
import LinkedInFix
import LinkedInBulkInsert_connections
#import LinkedInBulkInsert_perso
#import LinkedInBulkInsert_qualification
import LinkedInFix_perso

sys.path.insert(0, 'script/transformer/generic')
import Profile_vega
import Qualification_vega
import FriendsCollecting
import FriendBulkInsert
import TopicDetection
import TopicBulkInsert
import SentimentCollecting
import SentimentBulkInsert


if __name__ == '__main__':

	TwitterFix.fct()
	TwitterFix_perso.fct()

	FacebookFix.fct()
	FacebookFix_perso.fct()
	FacebookFix_postGrp.fct()

	LinkedInFix.fct()
	LinkedInFix_perso.fct()

	TwitterBulkInsert_follow.fct()
	TwitterBulkInsert_like.fct()
	#TwitterBulkInsert_perso.fct()
	TwitterBulkInsert_tweet.fct()

	FacebookBulkInsert_comment.fct()
	FacebookBulkInsert_follow.fct()
	FacebookBulkInsert_friend.fct()
	FacebookBulkInsert_like.fct()
	#FacebookBulkInsert_perso.fct()
	FacebookBulkInsert_post.fct()
	FacebookBulkInsert_postGrp.fct()
	FacebookBulkInsert_vote.fct()

	LinkedInBulkInsert_connections.fct()
	#LinkedInBulkInsert_perso.fct()


	Profile_vega.fct()
	Qualification_vega.fct()
	FriendsCollecting.fct()
	FriendBulkInsert.fct()
	TopicDetection.fct()
	TopicBulkInsert.fct()
	SentimentCollecting.fct()
	SentimentBulkInsert.fct()

