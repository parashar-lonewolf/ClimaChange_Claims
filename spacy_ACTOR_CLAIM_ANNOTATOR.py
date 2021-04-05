#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat Mar 27 13:25:00 2021
@author: de.illusionist
"""


## Local-index     	: ConLL notations
## <<actor>>	   	: B-ACT, I-ACT
## //claim// 		: B-CLAIM, I-CLAIM
## everything else	: O


## Libraries
import spacy
import requests
import PySimpleGUIQt as sg
import os

####################################################################
## READ ME FOR USAGE :
## python -m pip install PySimpleGUIQt // for gui lib installation
## The first window will have ask
## WINDOW 1. 
## "'So do you think this has a CLAIM ?'
## You answer yes by selecting a new actor and/or just clicking "Next"
## WINDOW 2
##   'Select the Claim boundaries'
## This brings us to the claim annotations, where we have to select the words to be used as boundaries
##
## if you select "Cancel" at WINDOW 1, you remove that sentence from tagging criterias.
## if you select "Exit" the prgram ends and only writes till last completely tagged article
##
############################################################################################
## ADJUST THESE AS PER YOUR NEED				  ####			  ##
############################################################################################
## Source										  ##
file_text = open("NYT_KyotoConferenceData_clean.txt").read()				  ##
textlist = file_text.splitlines()							  ##
SAVE_DATA = "Kyoto_progress_manager.txt"						  ##
OUTPUT_FILE = "NYT_KyotoConferenceData_annotated.txt"		  			  ##
ConLL_FILE = "NYT_KyotoConferenceData_ConLL.txt"				  	  ##
											  ##
############################################################################################
## ADJUST THESE AS PER YOUR NEED 				  ####			  ##
############################################################################################
restart_index = 0
if(os.path.exists(SAVE_DATA)):
	save_text = open(SAVE_DATA).read()
	save_text = save_text.split()
	restart_index = int(save_text[0])
	print("restart_index :"+str(restart_index))

#half = int(len(textlist)/2)+(len(textlist)%2)
#Ian_textlist = textlist[:(half+(2*restart_index))]
#Ank_textlist = textlist[(half+(2*restart_index)):]
####################################################################
##sg.Window(title='Loading', background_color='#FFFFFF', layout=layout, size=(500, 250), location=window_location)
## GUI for annotation
def gui_creator(text,save_text,ident):
	## basic properties of windows
	location = (200,500)
	size=(800, 800)
	num_buttons = []
	## splitting the text for buttoning them up
	for t in text.split():
		if( t == "<ACTOR>" or t == "<CANDIDATE>"):
			num_buttons.append(sg.Button(t,button_color=('white', 'black')))
		else:
			num_buttons.append(sg.Button(t,button_color=('black', 'white')))
	l = len(num_buttons)
	save_data = save_text.split()
	PROGRESS_BAR = save_data[0]+" article out of "+save_data[1]+"\t||\t"+save_data[3]+" lines out of "+save_data[2]+"\t||\t"+save_data[4]+" valid sentences"
	## For tagging Claim, begin and end words 
	if(ident == 'CLAIM'):
		mText = 'Select the Claim boundaries'
		logo = "WINDOW 2 \nSelect the words to be used as claim sequence boundaries"
		return_words = []
		return_index = []
		layout = [[sg.Text(logo), sg.Text('', key='_OUTPUT_',size=(65,1))],
			[i for i in num_buttons[:(int(l/4)+(l%4))]],
			[j for j in num_buttons[(int(l/4)+(l%4)):2*(int(l/4)+(l%4))]],
			[k for k in num_buttons[2*(int(l/4)+(l%4)):3*(int(l/4)+(l%4))]],
			[h for h in num_buttons[3*(int(l/4)+(l%4)):4*(int(l/4)+(l%4))]],
        	        [ sg.Button('Pro Environment',button_color=('gold', 'Red')),sg.Button('Against Environment',button_color=('yellow', 'black'))],
        	        [ sg.Button('Next',button_color=('yellow', 'Red'))],
        	        [sg.Button('Exit',button_color=('yellow', 'Red'))],
        	        [sg.Button('Save Prev annotations',button_color=('Red', 'white'))],
        	        [sg.Text(PROGRESS_BAR), sg.Text('', key='_OUTPUT_',size=(65,1))]]
		window = sg.Window(mText,size=size, location=location).Layout(layout)
		#window.Maximize()
		##################################
		## Event Loop for taking in words for claim tagging
		event_tracker = -5
		while True:             # Event Loop
    			event, values = window.Read()
    			print(event, values)
    			if event == 'Save Prev annotations':
        			SAVE_DATA_fun(save_text)
        			
    			elif event == 'Exit':
        			return_stuff = ('Exit',0)
        			break
    			elif event is None or event == 'Next':
        			return_stuff = (return_words, return_index)
        			break
    			else:
        			cur_trac = num_buttons.index(window.FindElement(str(event)))
        			tt = text.split()[cur_trac]

        			return_words.append((text.split(" ")[cur_trac]))
        			return_index.append(cur_trac)
        			window.FindElement(str(event)).Update(button_color=('black', 'yellow'))
        			event_tracker = num_buttons.index(window.FindElement(str(event)))
	## For tagging actor and accepting a sentence for tagging 
	elif(ident == 'ACTOR'):
		mText = 'is there a CLAIM ?'
		logo = "WINDOW 1 \nYou answer yes by selecting a new actor and/or just clicking 'Next' or 'Cancel' if not a claim"
		return_words = ""
		return_index = []
		layout = [[sg.Text(logo), sg.Text('', key='_OUTPUT_',size=(65,1))],
			[i for i in num_buttons[:(int(l/4)+(l%4))]],
			[j for j in num_buttons[(int(l/4)+(l%4)):2*(int(l/4)+(l%4))]],
			[k for k in num_buttons[2*(int(l/4)+(l%4)):3*(int(l/4)+(l%4))]],
			[h for h in num_buttons[3*(int(l/4)+(l%4)):4*(int(l/4)+(l%4))]],
        	        [ sg.Button('Next',button_color=('yellow', 'Red')),sg.Button('Cancel',button_color=('yellow', 'Red'))],
        	        [sg.Button('Exit',button_color=('yellow', 'Red'))],
        	        [sg.Button('Save Prev annotations',button_color=('Red', 'white'))],
        	        [sg.Text(PROGRESS_BAR), sg.Text('', key='_OUTPUT_',size=(65,1))]]
		window = sg.Window(mText,size=size, location=location).Layout(layout)
		##################################
		## Event Loop for taking in words for claim tagging
		while True:             # Event Loop
    			event, values = window.Read()
    			print(event, values)
    			if event == 'Save Prev annotations':
        			SAVE_DATA_fun(save_text)

    			elif event == 'Exit':
        			return_stuff = ('Exit',0)
        			break
    			elif event is None or event == 'Next':
        			return_stuff = (return_words, return_index)
        			break
    			elif event == 'Cancel':
        			return_stuff = ('Cancel',0)
        			break
    			else:

        			cur_trac = num_buttons.index(window.FindElement(str(event)))
        			tt = text.split()[cur_trac]
        			return_index.append(cur_trac)
        			print("tt: "+tt)
        			if(len(return_words)==0):
        				return_words = return_words+tt
        				print("return_words :"+return_words)
        			else:
        				return_words = return_words+" "+tt
        				print("return_words :"+return_words)
#        			return_words = return_words+str(event)+" "
        			window.FindElement(str(event)).Update(button_color=('yellow', 'blue'))



	window.Close()
	return return_stuff

#########################CONVERT MARKERS TO TAGS#############################
def convert_to_ConLL(doc, new_text, index, a, b):
	
	ConLL_data = ""

	a_index = [len(a.split()),len(a.split())+len(b.split())]
	## iterate through document 
	for sent in doc.sents:
        	## C_l = no of claim pairs
		k = -1
		c_l = len(index)
		if(c_l==2):
	        	cl_ind = 1
		else:
	        	cl_ind = 2
		
		for i, word in enumerate(sent):
	        	Actor_claim_tag = 'O'
                	########if punct, no word count#######
	        	if(str(word.dep_)!='punct' and c_l !=0):
                        	k+=1
                        	########if claim#######1st claim per actor
                        	if(k >= index[0] and k <= index[1]):
                        	        if(k == index[0]):
                        	                Actor_claim_tag = "B-CLAIM"
                        	        else:
                        	                Actor_claim_tag = "I-CLAIM"
                        	########if actor#######
                        	elif(k >= a_index[0] and k < a_index[1]):
                        	        if(k == a_index[0]):
                        	                Actor_claim_tag = "B-ACT"
                        	        else:
                        	                Actor_claim_tag = "I-ACT"
                        	if(cl_ind == 2):
                        	        ########if claim#######2nd claim per actor
                        	        if(k >= index[2] and k <= index[3]):
                        	                if(k == index[2]):
                        	                        Actor_claim_tag = "B-CLAIM"
                        	                else:
                        	                        Actor_claim_tag = "I-CLAIM"

	        	ConLL_data += str("%d\t%s\t%s\t%s\t%s\t%s\n"%(
	        	i+1, # There's a word.i attr that's position in *doc*
	        	word,
	        	word.tag_, # Fine-grained tag
	        	word.ent_type_,
	        	word.dep_, # Relation
                  	Actor_claim_tag # Relation
	        	))
	text_file = open(ConLL_FILE, "a")
	text_file.write(ConLL_data)
	text_file.close()
	return 0

######################SAVE ANNOTATION HISTORY###########################
def SAVE_DATA_fun(save_data):
	text_file = open(SAVE_DATA, "w")
	text_file.write(save_data)
	text_file.close()
	return 0

####################################################################
## Language model
nlp = spacy.load('en_core_web_sm') 

####################################################################
## Empty lists for storing processed text
full_text = []
full_text_2 =[]
n_cnt = 1
tot_articles = len(textlist)
##################################
## for checking and restarting annotation from save checkpoint
saved_anno = False
if(os.path.exists(SAVE_DATA)):
	n_cnt = restart_index
	saved_anno = True
	tot_articles = int(save_text[1])
	n_line = int(save_text[2])
	progress_line = int(save_text[3])
	found = int(save_text[4])
##################################

#save_data = (n_cnt,tot_articles,n_line,progress_line,found)
##################################
## for iterating per paragraph in text
#def textlist_iter(i):

for i in textlist[2*restart_index:]:
	fin_text   = ""
	new_text_2 = ""
	##################################
	## for non-zero input from text        	
	if(len(i)>0):
		# default initialize for func: convert_to_ConLL(doc, new_text, ind, a, b)
		a = ""
		b = ""
		ind = []
		## temp variables per article/paragraph
		p = i
		## convert paragraph to sentences
		para = [sent for sent in nlp(p).sents]
		n_line = len(para)
		if(not saved_anno):
			progress_line = 0
			found = 0
		elif(saved_anno):
			para = para[progress_line:]
			saved_anno = False
		##################################
		for sen in para:
			progress_line += 1
			s = str(sen)
			doc = nlp(s)
			sen_bin = 0  ## binary for a new sentence
			k = doc.ents
			labels = []
			yesno = [0,0] ## for checking if a sent has PER/ORG
			##################################
	        	## for checking if sent is useful
			for entity in k:
			        if(str(entity.label_) == "ORG" or str(entity.label_) == "PERSON"):
			        	yesno[0]=1
			        	found += 1
			        	print("FOUND")
			        	break
			        yesno[1]+=1

	        	##################################
			## if PER/ORG is not there, just write the sentence down
	        	## default sentence
			temp_text_0 = s
			if(yesno[0] == 0):
			        print("NOT FOUND")
			        new_text_2  = new_text_2 + "\n" + temp_text_0
			##################################
			## if PER/ORG found, ANNOTATE
			else:
			        ent = k[yesno[1]]
			        ## indexes to use (ent.start_char, ent.end_char)
				## printing the entire sentence,if tags found
			        x = ent.start_char-1
			        if(x<0):
			        	x = 0
			        y = ent.end_char
			        a = str(s[0:x])
			        b = ent.text
			        c = str(s[(y+1):])
			        temp_text_1 = a +" <CANDIDATE> "+b+" <ACTOR> "+c
			        
	        	        ##################################
	        	        ## Taking input from USER for annotation from GUI
			        save_data = str(n_cnt)+" "+str(tot_articles)+" "+str(n_line)+" "+str(progress_line-1)+" "+str(found-1)
			        yn, a_ind = gui_creator(temp_text_1,save_data,'ACTOR')			## Tag ACTOR GUI CALL
			        nn = ""								## default value for error control
			        ##############################
	        	        ## if ACCEPTED for tagging
			        if(yn!='Cancel' and yn!='Exit'):
	        	        	##################################
	        	        	## if the answer is "yes" = "z"
	        	        	if(len(yn)>0):
						#actor_crction = "<SUGGESTED ACTOR> "+str(yn)+"\n"
	        	        		x = s.find(yn[:-1])-1
	        	        		if(x<0):
	        	        			x = 0
	        	        		y = x + len(yn)+1
	        	        		a = s[0:x]
	        	        		b = yn
	        	        		c = s[(y):]
	        	        		temp_text_1 = a +" <CANDIDATE> "+b+" <ACTOR> "+c

	        	        	else:
	        	        		yn = b
	        	        	##################################
	        	        	## for annotating the claims
	        	        	nn, ind = gui_creator(temp_text_1,save_data,'CLAIM')		## Tag CLAIM GUI CALL
	        	        	if(nn == 'Exit'):
	        	        		break
	        	        	claims = nn
	        	        	##################################
	        	        	s2 = []		## temporary sentence for post-tag wriiting to file
	        	        	xx = 0		## temp variable to break sentence(S) into parts
	        	        	cl_count = 1  	## claim tag variable
	        	        	t_split = temp_text_1.split()
	        	        	actor_done = 0
	        	        	a_i = a.split()  	## the part of sentence before the actor
	        	        	b_i = b.split()  	## the actor
	        	        	##################################### Converting GUI input into marker Tags #########################################
	        	        	for i in ind:
	        	        		#####################################
	        	        		## EVEN NUMBER COUNT:2,4
	        	        		if((cl_count%2)==0):	########## sequence in which they might appear
	        	        			if(i<len(a_i)):		## COUNT 2
	        	        				temp = t_split[xx:(i-1)]+[" "+t_split[i]+"//\n"]
	        	        				s2 += temp							########## 2
	        	        				xx = i+1
	        	        				s2+= t_split[xx:len(a_i)]+[" \n<<"+b+">>\n "]			########## 3
	        	        				xx = len(a_i)+len(b_i)+2
	        	        				actor_done = 1
	        	        			else:			## COUNT 4
	        	        				temp = t_split[xx:(i-1)]+[" "+t_split[i]+"//\n"]+t_split[(i+1):]
	        	        				s2 += temp							########## 6
	        	        				xx = i
	        	        		#####################################
	        	        		## ODD NUMBER COUNT:1,3
	        	        		else:
	        	        			if(i<len(a_i)):		## COUNT 1
	        	        				temp = t_split[xx:i]+[" \n//"+t_split[i]+" "]
	        	        				s2 += temp							########## 1
	        	        				xx = i+1
	        	        			else:
	        	        				if(actor_done == 0 ):		## COUNT 3
	        	        					s2+= t_split[xx:len(a_i)]+[" \n<<"+b+">>\n "]		########## 4
	        	        					xx = len(a_i)+len(b_i)+2
	        	        					actor_done = 1
	        	        				temp = t_split[xx:i]+[" \n//"+t_split[i]+" "]
	        	        				s2 += temp							########## 5
	        	        				xx = i+1


	        	        		## claim tag count
	        	        		cl_count += 1

	        	        	###############################################################################################################

	        	        	temp_text_1 = " ".join(s2)
	        	        	print(temp_text_1) 

	        	        	##################################
	        	        	## for the BIG TEXT variable to be written later
	        	        	new_text_2 =  new_text_2 + "\n" + temp_text_1
	        	        	## covert and tag the conLL format
	        	        	convert_to_ConLL(doc, temp_text_1, ind, a, b)

	        	        ##############################
	        	        ## if NOT ACCEPTED for tagging
			        elif(yn=='Exit'):
	        	        	break
			        else:
	        	        	new_text_2 =  new_text_2 + "\n" + temp_text_0
	        	        	## covert and tag the conLL format
	        	        	convert_to_ConLL(doc, temp_text_0, ind, a, b) 
	        	        	#break


		if(nn == 'Exit' or yn == 'Exit'):
	        	break
		fin_text = new_text_2
		n_cnt +=1
		## human tag format
		text_file_2 = open(OUTPUT_FILE, "a")
		text_file_2.write(fin_text)
		text_file_2.close()
        	

