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
          Instructions for using the Annotator :
#####################################################################################################
              The first window will have ask
WINDOW 1. 
"'So do you think this has a CLAIM ?'

      1. You answer yes by selecting a new actor and/or just clicking "Next"

WINDOW 2
'Select the Claim boundaries'

    2. This brings us to the claim annotations, where we have to select the words to be used as boundaries, i.e
    the first word and the last word of the claim sequence.
    For eg: Ryan Uchiha said "The world is going to hell"
          you select ["The] and [hell"] on the window. and click on "Next"

3. if you select "Cancel" at WINDOW 1, you remove that sentence from tagging criterias.
4. if you select "Exit" the prgram ends and only writes till last completely tagged article
5. If you select save, it will save all current progress of dataset annotations,
 and once you exit and restart, the annotation will continue from the last annotation point.
6. In case, you made a mistake in the annoatation, the current version addresses the issue as:
            a.  Click on "Save Prev Annotations"
            b. press "Exit"
            c. rerun the annotator program
#######################################################################################################
