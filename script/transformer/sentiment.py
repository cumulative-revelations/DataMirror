#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import common as c

analyzer = SentimentIntensityAnalyzer()

def getVal(text):
	return (text['compound'])

def getSentiment(myText):
	string = ""
	val = 0
	neg = 0
	pos = 0
	neu = 0

	myText=c.cleanText(myText)
	part = myText.split("\t")

	if len(part) >1:
		text = part[0].strip()
		date = part[1].strip()

		vs = analyzer.polarity_scores(text)
		val = getVal(vs)

		neg = vs['neg']
		pos = vs['pos']
		neu = vs['neu']

	#string= '{"senti":"'+str(val)+'","pos":"'+str(pos)+'","neg":"'+str(neg)+'","neu":"'+str(neu)+'","loadSource":"twitter"'+'}'

	return val,pos,neu,neg



