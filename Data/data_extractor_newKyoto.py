#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Jan 3 13:44:00 2021
@author: de.illusionist
"""

from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import numpy as np
import requests


def _main():
	n = 0
	f = 'filename will arive in this variable'
	while(len(f)>0):
		f = datareader_xml(n)
		tagnavigator_xml(f)
		n = n + 1
	return 0
	

def datareader_xml(n):
	filename_data = open("filenames.txt").read()
	filelist = filename_data.split()
	return("climate/"+filelist[n])


def tagnavigator_xml(filename):
	with open(filename, 'r') as f:
		text = f.read()
		soup = BeautifulSoup(text)
		tag_body = soup.find("body")

		## headline and abstract
		tag_headline = tag_body.find("body.head")
		headline = printallchildren_xml(tag_headline, "hl1")
		abstract = printallchildren_xml(tag_headline, "abstract")

		## CONTENT	
		tag_content = tag_body.find("body.content")
		content = printallchildren_xml(tag_content, "p")

		towrite = [headline,abstract,content]
#		folder = str("clean_data"+"/"+ filename[9:-4])
		if "Kyoto" in content:
			writetofile(filename,towrite)
#		for child in tag_body.recursiveChildGenerator():
#			if child.name:
#				print(child.name)
	return 0


def printallchildren_xml(tag, children):
	#print("\n \nThis ",str(children)," for ",f"{tag.name}","\n \n")
	text = ''
	for tag in tag.find_all(children):
#        	print(f'{tag.text}')
		text = text + f'{tag.text}'
	return text

def writetofile(filename,towrite):
	name = "4mFullData_Kyotoclean_data"
	namelist = [name+"_head.txt",name+"_abstract.txt",name+"_content.txt"]
	count = list({0,1,2})
	name_file = open("4mFullData_Kyoto_filename_list.txt", "a")
	name_file.write(filename+"\n")
	name_file.close()
	print(filename)
	for i in count:
		text_file = open(namelist[i], "a")
		text_file.write("\n\n\n"+ towrite[i])
		text_file.close()
	return 0

_main()

############################

