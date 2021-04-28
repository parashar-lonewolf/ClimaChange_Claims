#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat Mar 20 15:05:00 2021
@author: de.illusionist, cloppy2
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
from screeninfo import get_monitors
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
############################################################################################
############################################################################################
## 					MAIN FUNCTION 					  ##
############################################################################################
def _main():
	############################################################################################
	## ADJUST THESE AS PER YOUR NEED 				  ####			  ##
	############################################################################################
	## Source										  ##
	file_text = open("Data/4mFullData_NYT_KyotoConferenceData_cleaned.txt").read()				  ##										  ##
	file_dates = open("Data/4mFullData_Kyoto_filename_list.txt").read()				  ##
	textlist = file_text.split("\n\n")							  ##
	dateslist = file_dates.splitlines()							  ##
	SAVE_DATA = "Save/Progress_manager.txt"						  ##
	OUTPUT_FILE = "Save/Localformat_annotator.txt"	
	ConLL_FILE = "Save/ConLLformat_annotator.txt"		  			  ##
	CLAIM_FILE = "Save/Claims.txt"				  	  ##
	############################################################################################
	restart_index = 1
	if(os.path.exists(SAVE_DATA)):
		save_text = open(SAVE_DATA).read()
		save_text = save_text.split()
		restart_index = int(save_text[0])
		print("restart_index :"+str(restart_index))
	
	#half = int(len(textlist)/2)+(len(textlist)%2)
	#Ank_textlist = textlist[:(half+restart_index)]
	#Ian_textlist = textlist[(half+restart_index):]
	#Ank_dateslist = dateslist[:(half+restart_index)]
	#Ian_dateslist = dateslist[(half+restart_index):]
	####################################################################

	## Language model
	nlp = spacy.load('en_core_web_sm') 

	####################################################################
	## Empty lists for storing processed text
	n_cnt = 1
	n_line = 0
	progress_line = 0
	found = 0
	##################################
	## for checking and restarting annotation from save checkpoint
	saved_anno = False
	tot_articles = len(textlist)
	if(os.path.exists(SAVE_DATA)):
		n_cnt = restart_index
		saved_anno = True
		tot_articles = int(save_text[1])
		n_line = int(save_text[2])
		progress_line = int(save_text[3])
		found = int(save_text[4])

	temp = 1
	count = restart_index-1
	#if restart_index != 0: 
	#	count = restart_index-1
	claim_nos = 0
	while(n_cnt!=0):
		i=textlist[count]
		date="/".join((dateslist[count].split("/")[1][:-4]).split("_")[:4])
		n_cnt,found,saved_anno,claim_nos = repeat_annotator(claim_nos,date,i,nlp,saved_anno,n_cnt,tot_articles,n_line,progress_line,found,file_dates,CLAIM_FILE,SAVE_DATA,OUTPUT_FILE,ConLL_FILE)
		count+=1
	return 0

############################################################################################
## 					GUI FUNCTION 					  ##
############################################################################################

## GUI for annotation
def gui_creator(text,save_text,ident,SAVE_DATA):
	print("#################################")
	print(text)
	print("#################################")
	## basic properties of windows
	location = (1920/6,1080/3)
	size=(1920/4,1080/4)
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
	if(ident == 'CLAIM' or ident == 'AGAIN CLAIM'):
		again_text = ''
		if(ident == 'AGAIN CLAIM'):             # claim boundaries not selected text
    			again_text = "NOT SELECTED PROPER CLAIM BOUNDARIES ERROR: Please select again, "
		Pol = '0'
		mText = again_text+'Select the Claim boundaries:'
		logo = "WINDOW 2 \nSelect the words to be used as \"the claim\" boundaries\nFormat:\n1. ..<actor>..(.<word.i>...to...<word.n>..)*k.times\n2. (.<word.i>...to...<word.n>..)*k.times...<actor>..\n3. ..(.<word.i>...to...<word.n>..)*k.times...<actor>...(<word.j>...to...<word.m>)*l.times.."
		return_words = []
		return_index = []
		layout = [[sg.Text(logo), sg.Text('', key='_OUTPUT_',size=(65,1))],
			[i for i in num_buttons[:(int(l/4)+(l%4))]],
			[j for j in num_buttons[(int(l/4)+(l%4)):2*(int(l/4)+(l%4))]],
			[k for k in num_buttons[2*(int(l/4)+(l%4)):3*(int(l/4)+(l%4))]],
			[h for h in num_buttons[3*(int(l/4)+(l%4)):4*(int(l/4)+(l%4))]],
			[sg.Text("Does the ACTOR, SUPPORT or is AGAINST the CLAIM?\t\t(there is no default value)"), sg.Text('', key='_OUTPUT_',size=(65,1))],
        	        [ sg.Button('[Supports]',button_color=('gold', 'Red')),sg.Button('[Against]',button_color=('yellow', 'black'))],
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
    			print(Pol)
    			event, values = window.Read()
    			print(event, values)
    			if event == 'Save Prev annotations':
        			SAVE_DATA_fun(save_text,SAVE_DATA,'w')
        			
    			elif event == 'Exit' or event == None:
        			SAVE_DATA_fun(save_text,SAVE_DATA,'w')
        			return_stuff = ('Exit',0,'')
        			break
    			elif event == 'Next':
        			if Pol == '0':
        				print("Choose supports or against")
        			else:
        				return_index.sort()
        				return_stuff = (return_words,return_index ,Pol)
        				break
    			elif event == '[Supports]' or event == '[Against]':
        			if event == '[Supports]':
        				Pol = '+'

        			elif event == '[Against]':
        				Pol = '-'
        			
    			else:
        			cur_trac = num_buttons.index(window.FindElement(str(event)))
        			tt = text.split()[cur_trac]

        			return_words.append((text.split(" ")[cur_trac]))
        			return_index.append(cur_trac)
        			window.FindElement(str(event)).Update(button_color=('black', 'yellow'))
        			event_tracker = num_buttons.index(window.FindElement(str(event)))
    			SAVE_DATA_fun(save_text,SAVE_DATA,'w')
	## For tagging actor and accepting a sentence for tagging 
	elif(ident == 'ACTOR'):
		mText = 'Is there a Claim in the sentence ?'
		logo = "WINDOW 1 \nYou answer yes by selecting a new actor (select the word(s)) and/or just clicking 'Next' or 'Cancel' if not a claim"
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
        			SAVE_DATA_fun(save_text,SAVE_DATA,'w')

    			elif event == 'Exit' or event == None:
        			SAVE_DATA_fun(save_text,SAVE_DATA,'w')
        			return_stuff = ('Exit',0)
        			break

    			elif event == 'Next':
        			w = return_words.split()
        			wd = dict(zip(return_index,w))
        			return_index.sort()
        			return_words = (" ").join([wd[i] for i in return_index])
        			return_stuff = (return_words, return_index)
        			break
    			elif event == 'Cancel':
        			return_stuff = ('Cancel',0)
        			break
    			else:

        			cur_trac = num_buttons.index(window.FindElement(event))
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
    			SAVE_DATA_fun(save_text,SAVE_DATA,'w')



	window.Close()
	return return_stuff
############################################################################################
## 					ConLL tag FUNCTION 				  ##
############################################################################################

#########################CONVERT MARKERS TO TAGS#############################
def convert_to_ConLL(doc, new_text, new_tag, a, b, pol, ConLL_FILE,date):
	
	ConLL_data = ""

	a_index = [len(a.split()),len(a.split())+len(b.split())]
	## iterate through document 
	for sent in doc.sents:
        	## C_l = no of claim pairs
		B_act = 0
		B_claim = 0
		k = -1
		hyp = 0
		new_i = new_tag.split("\n")
		date_done = 0

		for i, word in enumerate(sent):
	        	Actor_claim_tag = 'O\t'
                	########if punct, no word count#######
	        	if(len(new_i)>1):
                        	
                        	if(str(word)[0]=="'" and str(word.dep_)!='punct'):
                        		Actor_claim_tag = new_i[k]

                        	elif(str(word.dep_)!='punct' and str(word.tag_) != 'HYPH' and hyp == 0):
                        		k+=1
                        		try:
                        			Actor_claim_tag = new_i[k]
                        		except:
                        			k-=1
                        			Actor_claim_tag = new_i[k]

                        	elif(str(word.tag_) == 'HYPH' or hyp == 1):
                        		if(hyp == 1):
                        			hyp = 0
                        			Actor_claim_tag = new_i[k]
                        		else:
                        			hyp = 1
                        			Actor_claim_tag = new_i[k]
                        		if(new_i[k][0] == "B"):
                        			Actor_claim_tag = "I"+new_i[k][1:]
	        	if(i==0 and date_done ==0):
                        	Actor_claim_tag += "\t"+date		## beginning of each sentence tagged with the date
                        	date_done = 1

	        	ConLL_data += str("%d\t%s\t%s\t%s\t%s\t%s\n"%(
	        	i+1, # There's a word.i attr that's position in *doc*
	        	word,
	        	word.tag_, # Fine-grained tag
	        	word.ent_type_,
	        	word.dep_, # Relation
                  	Actor_claim_tag # Actor/claim tag
	        	))
	text_file = open(ConLL_FILE, "a")
	text_file.write(ConLL_data)
	text_file.close()
	return 0
############################################################################################
## 					SAVE DATA FUNCTION 					  ##
############################################################################################

######################SAVE ANNOTATION HISTORY###########################
def SAVE_DATA_fun(save_data,SAVE_DATA,mode):
	text_file = open(SAVE_DATA, mode)
	text_file.write(save_data)
	text_file.close()
	return 0



############################################################################################
## 					the main ITERATOR 				  ##
############################################################################################
#def textlist_iter(i):
def repeat_annotator(claim_nos,date,i,nlp,saved_anno,n_cnt,tot_articles,n_line,progress_line,found,file_dates,CLAIM_FILE,SAVE_DATA,OUTPUT_FILE,ConLL_FILE):

	yn = ""
	nn = ""
	##################################
	## for non-zero input from text        	
	if(len(i)>0):
		print("Article no :"+str(n_cnt))
		text_file_2 = open(OUTPUT_FILE, "a")
		text_file_2.write(str("\nArticle no :"+str(n_cnt)+"\n"))
		text_file_2.close()
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
			print("not")
			progress_line = 0
			found = 0
		elif(saved_anno):
			print("yes")
			progress_line-=1
			para = para[progress_line:]
			saved_anno = False
		##################################
		for sen in para:
			the_claim = '' 		## claim variable for claim collection
			no_claims = 0
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
			        if(str(entity.label_) == "ORG" or str(entity.label_) == "PER" or str(entity.label_) == "PERSON"):
			        	yesno[0]=1
			        	found += 1
			        	#print("FOUND")
			        	break
			        yesno[1]+=1

	        	##################################
			## if PER/ORG is not there, just write the sentence down
	        	## default sentence
			temp_text_0 = s
			if(yesno[0] == 0):
			        print("NOT FOUND")
			        convert_to_ConLL(doc, temp_text_0, '', '', '', '', ConLL_FILE,date)
			        text_file_2 = open(OUTPUT_FILE, "a")
			        text_file_2.write(temp_text_0)
			        text_file_2.close()
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
			        b = ent.text 		## actor variable for actor collection
			        c = str(s[(y+1):])
			        temp_text_1 = a +" <CANDIDATE> "+b+" <ACTOR> "+c
			        
	        	        ##################################
	        	        ## Taking input from USER for annotation from GUI
			        ## CURRENT ARTICLE NUMBE| TOTAL NO OF ARTICLES| TOTAL NO OF LINES IN CURRENT ARTICLES| CURRENT LINE NO IN ARTICLE| NO OF VALID CANDIDATE SENTENCES FOUND
			        save_data = str(n_cnt)+" "+str(tot_articles)+" "+str(n_line)+" "+str(progress_line)+" "+str(found)
			        yn, a_ind = gui_creator(temp_text_1,save_data,'ACTOR',SAVE_DATA)			## Tag ACTOR GUI CALL
			        nn = ""								## default value for error control
			        temp_text_split = temp_text_1.split()
			        
			        print("Prints:\taa,bb,cc")
			        ##############################
	        	        ## if ACCEPTED for tagging
			        if(yn!='Cancel' and yn!='Exit'):
	        	        	##################################
	        	        	## if the answer is "yes" = "z"
	        	        	if(len(yn)>0):
	        	        		aa = temp_text_split[:a_ind[0]]
	        	        		print(aa)
	        	        		try:
	        	        			aa.remove("<CANDIDATE>")
	        	        		except:
	        	        			print("")
	        	        		try:
	        	        			aa.remove("<ACTOR>")
	        	        		except:
	        	        			print("")

	        	        		a = (" ").join(aa)
	        	        		bb = temp_text_split[a_ind[0]:(a_ind[-1]+1)]
	        	        		print(bb)
	        	        		try:
	        	        			bb.remove("<CANDIDATE>")
	        	        		except:
	        	        			print("")
	        	        		try:
	        	        			bb.remove("<ACTOR>")
	        	        		except:
	        	        			print("")
	        	        		b = (" ").join(bb)
	        	        		cc = temp_text_split[(a_ind[-1]+1):]
	        	        		print(cc)
	        	        		try:
	        	        			cc.remove("<CANDIDATE>")
	        	        		except:
	        	        			print("")
	        	        		try:
	        	        			cc.remove("<ACTOR>")
	        	        		except:
	        	        			print("")
	        	        		c = (" ").join(cc)
	        	        
	        	        		temp_text_1 = a +" <CANDIDATE> "+b+" <ACTOR> "+c
	        	        		print(temp_text_1)

	        	        	else:
	        	        		yn = b 		## actor variable for actor collection
	        	        	##################################
	        	        	## for annotating the claims
	        	        	nn, ind, pol = gui_creator(temp_text_1,save_data,'CLAIM',SAVE_DATA)		## Tag CLAIM GUI CALL
	        	        	#print("\nnn is "+str(nn))
	        	        	#print("\nind is "+str(ind))
	        	        	if(nn == 'Exit'):
	        	        		return (0,found,saved_anno,claim_nos)
	        	        	while(ind == [] or len(nn)==0):
	        	        		nn, ind, pol = gui_creator(temp_text_1,save_data,'AGAIN CLAIM',SAVE_DATA)		## Tag CLAIM GUI CALL untill valid claim boundaries
	        	        		if(nn == 'Exit'):
	        	        			return (0,found,saved_anno,claim_nos)

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
	        	        	new_tag = ""
	        	        	the_claim = "## "+str(claim_nos+1)+" no Claim(s):\n"
	        	        	for i in ind:
	        	        		#####################################
	        	        		## EVEN NUMBER COUNT:2,4
	        	        		if((cl_count%2)==0):	########## sequence in which they might appear
	        	        			if(i<len(a_i)):		## COUNT 2
	        	        				temp = t_split[xx:(i-1)]+[" "+t_split[i]+"//\n"]
	        	        				the_claim += " ".join(t_split[xx:(i+1)])+"\n"
	        	        				no_claims += 1
	        	        				new_tag+=len(t_split[xx:(i+1)])*str("I-CLAIM\t"+pol+"\n")
	        	        				s2 += temp							########## 2
	        	        				xx = i+1
	        	        				if(actor_done == 0 ):		
	        	        					s2+= t_split[xx:len(a_i)]+[" \n<<"+b+">>\n "]		########## 3
	        	        					new_tag+=len(t_split[xx:len(a_i)])*"O\t\n"
	        	        					new_tag+="B-ACT\t\n"
	        	        					new_tag+=(len(b_i)-1)*"I-ACT\t\n"
	        	        					xx = len(a_i)+len(b_i)+2
	        	        					actor_done = 1
	        	        			else:			## COUNT 4
	        	        				temp = t_split[xx:(i-1)]+[" "+t_split[i]+"//\n"]
	        	        				the_claim += " ".join(t_split[xx:(i+1)])+"\n"
	        	        				no_claims += 1
	        	        				new_tag+=len(t_split[xx:(i+1)])*str("I-CLAIM\t"+pol+"\n")
	        	        				#new_tag+=len(t_split[(i+1):])*"O\t\n"
	        	        				s2 += temp							########## 6
	        	        				xx = i+1
	        	        		#####################################
	        	        		## ODD NUMBER COUNT:1,3
	        	        		else:
	        	        			if(i<len(a_i)):		## COUNT 1
	        	        				temp = t_split[xx:i]+[" \n//"+t_split[i]+" "]
	        	        				the_claim += t_split[i]+" "
	        	        				new_tag+=len(t_split[xx:i])*"O\t\n"
	        	        				new_tag+=str("B-CLAIM\t"+pol+"\n")
	        	        				s2 += temp							########## 1
	        	        				xx = i+1
	        	        			else:
	        	        				if(actor_done == 0 ):		## COUNT 3
	        	        					s2+= t_split[xx:len(a_i)]+[" \n<<"+b+">>\n "]		########## 4
	        	        					new_tag+=len(t_split[xx:len(a_i)])*"O\t\n"
	        	        					new_tag+="B-ACT\t\n"
	        	        					new_tag+=(len(b_i)-1)*"I-ACT\t\n"
	        	        					xx = len(a_i)+len(b_i)+2
	        	        					actor_done = 1
	        	        				temp = t_split[xx:i]+[" \n//"+t_split[i]+" "]
	        	        				the_claim += t_split[i]+" "
	        	        				new_tag+=len(t_split[xx:i])*"O\t\n"
	        	        				new_tag+=str("B-CLAIM\t"+pol+"\n")
	        	        				s2 += temp							########## 5
	        	        				xx = i+1


	        	        		## claim tag count
	        	        		cl_count += 1
	        	        	new_tag+=len(t_split[(i+1):])*"O\t\n"
	        	        	###############################################################################################################

	        	        	temp_text_1 = " ".join(s2)
	        	        	#print(temp_text_1) 

	        	        	##################################
	        	        	## for the BIG TEXT variable to be written later
	        	        	# new_text_2 =  new_text_2 + "\n" + temp_text_1
	        	        	## covert and tag the conLL format
	        	        	convert_to_ConLL(doc, temp_text_1, new_tag, a, b, pol, ConLL_FILE,date)
	        	        	claim_nos += no_claims
	        	        	SAVE_DATA_fun(the_claim+"#ACTOR: \'"+b+"\' HAS\t#"+str(no_claims)+" CLAIMS, DATED: "+date[:-3]+" \n\n",CLAIM_FILE,'a')
	        	        	text_file_2 = open(OUTPUT_FILE, "a")
	        	        	text_file_2.write(temp_text_1)
	        	        	text_file_2.close()
	        	        ##############################
	        	        ## if NOT ACCEPTED for tagging
			        elif(yn=='Exit'):
	        	        	return (0,found,saved_anno,claim_nos)
			        else:
	        	        	# new_text_2 =  new_text_2 + "\n" + temp_text_0
	        	        	## covert and tag the conLL format
	        	        	convert_to_ConLL(doc, temp_text_0, '', '', '', '', ConLL_FILE,date)
	        	        	claim_nos += no_claims
	        	        	#SAVE_DATA_fun(the_claim+"\nACTOR: "+b+" HAS\t#"+str(no_claims)+" CLAIMS, FROM "+date+" \n\n",CLAIM_FILE,'a')
	        	        	text_file_2 = open(OUTPUT_FILE, "a")
	        	        	text_file_2.write(temp_text_0)
	        	        	text_file_2.close()


		if(nn == 'Exit' or yn == 'Exit'):
	        	return (0,found,saved_anno,claim_nos)
		n_cnt +=1
		return (n_cnt,found,saved_anno,claim_nos)
	return (n_cnt,found,saved_anno,claim_nos)

###############################################################################################################
##################################PROGRAM RUN##################################################################
###############################################################################################################

_main()

###############################################################################################################
##################################PROGRAM END##################################################################
###############################################################################################################
