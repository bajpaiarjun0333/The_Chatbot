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
        



