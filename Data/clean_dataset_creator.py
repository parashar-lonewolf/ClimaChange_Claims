#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Mar 20 3:44:00 2021
@author: de.illusionist
"""


## index     : ConLL notations
## <actor>   : B-ACT, I-ACT
## //claim\\ : B-CLAIM, I-CLAIM
## else      : O


import numpy as np
import requests
import re

## The workflow
def _main(n):
	f_text = fullStopDetector()
	c_text = datasetCleaner(f_text,n)
	write_to_file(c_text)
	return 0

## Read and split the data into individual
def dataset_readnsplit():
	filename = "4mFullData_Kyotoclean_data_content.txt"
	file_data = open(filename).read()		
	textlist = file_data.split("\n\n\n")
	return textlist


## filter fullstops and add a " " after it so as to prevent stuff like:
## last word of prev sentence--->environments.To<---1st word of nxt sentence
def fullStopDetector():
	textlist = dataset_readnsplit()
	pattern = re.compile(r"[a-z0-9@\'?$%_)(;:][;\?%_)(\.:][a-zA-z]")
	new_text = "" 
	for para in textlist[1:]:		## for every paragraph/article
		temp_text = ""
		if(len(para)>0):
			find = pattern.search(para)
			text = para
			while(str(find)!='None'):
				index = find.span()
				print(index)
				temp_text = temp_text+text[:(index[0]+2)]+" "
				print(text[:(index[0]+2)])
				text = text[(index[1]-1):]
				find = pattern.search(text)
			temp_text = temp_text + text
			new_text = new_text + temp_text + "\n"
	return textlist[1]+"\n"+new_text


## Clean the data by removing repeating sentences at the beginning of paragraphs
## by comparing n-grams text
def datasetCleaner(textdata,n):
#	textlist = dataset_readnsplit()
	textlist = textdata.splitlines()
	new_text = ""
	for i in textlist:
		detected = 0
		if(len(i)>0):
			dtct = i[:n]
			for count in range(n,(len(i)-n)):
				source = i[count:(count+n)]
				if(dtct == source):
					detected = count
					break
			new_text = new_text + i[detected:] + "\n\n" 
	return new_text


## write cleaned data to a file
def write_to_file(textdata):
	text_file = open("4mFullData_NYT_KyotoConferenceData_cleaned.txt", "w")
	text_file.write(textdata)
	text_file.close()
	return 0

_main(15)

















