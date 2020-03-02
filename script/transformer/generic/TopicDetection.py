#!/usr/bin/env python3 
#-*- coding: utf-8 -*- 

"""
Created on Wed Dec 25 12:47:44 2019
@author: Amal Htait
"""

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import os, sys, json
sys.path.insert(0, '..')
import common as c

def clean(doc):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def getTopics(doc_complete):
    doc_clean = [clean(doc).split() for doc in doc_complete]   
    dictionary = corpora.Dictionary(doc_clean )

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=2, id2word = dictionary, passes=50)
    list_topics = ldamodel.print_topics(num_topics=2, num_words=30)
    arr_topics=[]
    for i in range(len(list_topics)):
        topics=list_topics[i][1].split("+")
        myArr=[]
        for j in range(len(topics)):
            parts = topics[j].strip().split("*")
            myArr.append(parts[1].strip('"'))
        arr_topics.append(myArr)

    return arr_topics




def fct():
    path = '../../dataSource/' 
    new_data = []

    try:

	    # Facebook
	    doc_complete_fb = []

	    json_file = open(path+'json-facebook_data/posts/your_posts_1.json', encoding="utf8", errors='ignore')
	    json_list = [line.strip() for line in json_file]

	    for doc in json_list:
	        json_doc = json.loads(doc)

	        if 'data' in json_doc:
	            for dt in json_doc['data']:
	                if 'post' in dt:
	                    my_text = dt["post"]
	                    doc_complete_fb.append(my_text)

	    fb_topics = getTopics(doc_complete_fb)

	    for i in range(len(fb_topics)):
	        for j in range(len(fb_topics[i])):
	            new_data.append({"topic_id": "fb_"+str(i) ,"topic_word" : c.cleanText(fb_topics[i][j]), "source" : "Facebook"})
	     


	    # tweets
	    doc_complete_tw = []

	    json_file = open(path+'json-twitter_data/tweet.json', encoding="utf8", errors='ignore')
	    json_list = [line.strip() for line in json_file]

	    for doc in json_list:
	        json_doc = json.loads(doc)

	        if not json_doc['full_text'].startswith("RT @"):
	        	my_text = json_doc["full_text"]
	        	doc_complete_tw.append(my_text)

	    tw_topics = getTopics(doc_complete_tw)

	    for i in range(len(tw_topics)):
	        for j in range(len(tw_topics[i])):
	            new_data.append({"topic_id": "tw_"+str(i) ,"topic_word" : c.cleanText(tw_topics[i][j]), "source" : "Twitter"})



	    string = ""
	    for mydata in new_data[:-1]:
	        string = string + str(mydata) + "\n"
	    string = string + str(new_data[-1])

	    string = string.replace("'",'"')


	    file_res = open('../../../vegaStuff/Topics.json',"w") 
	    file_res.write(string)
	    file_res.close()
	    print ("Collect Topics")

    except:
       print ("Error in Collect Topics")
       pass

