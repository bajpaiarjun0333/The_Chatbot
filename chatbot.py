#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 12:38:50 2019

@author: bajpaiarjun0333
"""

import tensorflow as tf
import numpy as np
import re
import time

#strating the data preprocessing 


#Importing the dataset
line_path='/home/bajpaiarjun0333/Artificial Intelligence/Chatbot/Corpus/movie_lines.txt'
conversation_path='/home/bajpaiarjun0333/Artificial Intelligence/Chatbot/Corpus/movie_conversations.txt'
lines=open(line_path).read().split('\n')
conversations=open(conversation_path).read().split('\n')

#creating a dictonary to map lines and it's id's
id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line)==5:
        id2line[_line[0]] = _line[4]

#Dictonary created to map line index to the line itself
conversations_ids=[]
#Creating a list of all the conversation without metadata
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    conversations_ids.append(_conversation.split(','))

#till now we the conversations and the mapping of the ids to the lines
"""In each conversation list we assume that the first integer is the question 
and the other is the answer"""

questions = []
answers = []

for conversation in conversations_ids:
    for i in range(len(conversation)-1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])

#we have our question and our answers ready to go

#implementing the phase 1 of data cleaning
def clean_text(text):
    text = text.lower()#converting the text to lower case
    text = re.sub(r"i'am","i am",text)
    text = re.sub(r"he's","he is",text)
    text = re.sub(r"she's","she is",text)
    text = re.sub(r"that's","that is",text)
    text = re.sub(r"what's","what is",text)
    text = re.sub(r"where's","where is",text)
    text = re.sub(r"\'ll"," will",text)
    text = re.sub(r"\'ve"," have",text)
    text = re.sub(r"\'re"," are",text)
    text = re.sub(r"\'d"," would",text)
    text = re.sub(r"won't","will not",text)
    text = re.sub(r"can't","cannot",text)
    text = re.sub(r"[-()\"#@;:<>+=|?.,~]","",text)
    return text
        
clean_questions = []
clean_answers = []
         
#cleaning the questions and the answers corresspondingly
for question in questions:
    clean_questions.append(clean_text(question))

for answer in answers:
    clean_answers.append(clean_text(answer))
    
#creating a frequency distribution of words in the conversation to avoid 
#extra words
word2count={}

for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word]+= 1

for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word]+= 1

#mapping each word in question and answer to seperate integer indices 
#to later encode or use word embedding
word_number = 0
questionswords2int = {}
answerswords2int = {}
threshold=20
for word,count in word2count.items():
    if count>=threshold:
        questionswords2int[word]=word_number
        word_number+=1
word_number=0        
for word,count in word2count.items():
    if count>=threshold:
        answerswords2int[word]=word_number
        word_number+=1

tokens=['<PAD>','<EOS>','<OUT>','<SOS>']

for token in tokens:
    questionswords2int[token]=len(questionswords2int)+1
    

for token in tokens:
    answerswords2int[token]=len(answerswords2int)+1

#creating the inverse mapping form int to words
answersints2word = {w_i:w for w,w_i in answerswords2int.items()}

#Adding the end of string to every answers

for i in range(len(clean_answers)):
    clean_answers[i]+=' <EOS>'
