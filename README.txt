## Install python virtualenv:
pip install virtualenv

## create a virtual environment
virtualenv climachange_env

## activate virtual environment
source climachange_env/bin/activate

## git clone repo
git clone https://github.com/parashar-lonewolf/ClimaChange_Claims.git

## move to folder
cd climachange_claims

## install requirements
pip install -r requirements.txt 

## Run Annotator
python  spacy_ACTOR_CLAIM_ANNOTATOR.py 

data_file: NYT_KyotoConferenceData_clean.txt
#####################################################################################################
## READ ME FOR USAGE :
## 					ANNOTATOR
#####################################################################################################
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
#######################################################################################################
