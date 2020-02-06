#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""


import TwitterFix
import TwitterFix_msg
#import TwitterFix_perso
import FacebookFix	
#import FacebookFix_perso		
import FacebookFix_postGrp

import TwitterBulkInsert_follow
import TwitterBulkInsert_like
import TwitterBulkInsert_msg
#import TwitterBulkInsert_perso
import TwitterBulkInsert_tweet
import FacebookBulkInsert_comment	
import FacebookBulkInsert_follow	
import FacebookBulkInsert_friend	
import FacebookBulkInsert_like	
import FacebookBulkInsert_msg	
#import FacebookBulkInsert_perso	
import FacebookBulkInsert_post
import FacebookBulkInsert_postGrp
import FacebookBulkInsert_vote




if __name__ == '__main__':
	TwitterFix.fct()
	TwitterFix_msg.fct()
	#TwitterFix_perso.fct()
	FacebookFix.fct()
	#FacebookFix_perso.fct()		
	FacebookFix_postGrp.fct()
	TwitterBulkInsert_follow.fct()
	TwitterBulkInsert_like.fct()
	#TwitterBulkInsert_msg.fct()
	#TwitterBulkInsert_perso.fct()
	TwitterBulkInsert_tweet.fct()
	FacebookBulkInsert_comment.fct()
	FacebookBulkInsert_follow.fct()
	FacebookBulkInsert_friend.fct()
	FacebookBulkInsert_like.fct()
	#FacebookBulkInsert_msg.fct()
	#FacebookBulkInsert_perso.fct()
	FacebookBulkInsert_post.fct()
	FacebookBulkInsert_postGrp.fct()
	#FacebookBulkInsert_vote.fct()


