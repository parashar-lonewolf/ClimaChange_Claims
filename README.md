### 1. Install python virtualenv:
pip install virtualenv

### 2. Create a virtual environment
virtualenv climachange_env

### 3. Activate virtual environment
source climachange_env/bin/activate

### 4. Create git clone repo
git clone https://github.com/parashar-lonewolf/ClimaChange_Claims.git

### 5. Move to folder
cd climachange_claims

### 6. Install requirements
pip install -r requirements.txt 

### 7. Run Annotator
python  spacy_ACTOR_CLAIM_ANNOTATOR.py 

data_file: NYT_KyotoConferenceData_clean.txt

## Instructions for using the Annotator :

## The first window will have ask
### WINDOW 1. 
"'So do you think this has a CLAIM ?'

1. You answer yes by selecting a new actor and/or just clicking "Next"
![Window 1](https://cdn.mathpix.com/snip/images/XGYC-RtOBgZ8Q6Q0gZakJ3YR16POXr2qbuO9ELTNdIo.original.fullsize.png)

### WINDOW 2
'Select the Claim boundaries'

2. This brings us to the claim annotations, where we have to select the words to be used as boundaries, i.e
the first word and the last word of the claim sequence.
For eg: Ryan Uchiha said "The world is going to hell"
you select ["The] and [hell"] on the window. and click on "Next"
![Window 2](https://cdn.mathpix.com/snip/images/zduy_IXZ26doytg3WnNLEIxekxwPJVuI8NptxbJReOU.original.fullsize.png)

3. if you select "Cancel" at WINDOW 1, you remove that sentence from tagging criterias.
4. if you select "Exit" the prgram ends and only writes till last completely tagged article
5. If you select save, it will save all current progress of dataset annotations,
and once you exit and restart, the annotation will continue from the last annotation point.
6. In case, you made a mistake in the annoatation, the current version addresses the issue as:
            a.  Click on "Save Prev Annotations"
            b. press "Exit"
            c. rerun the annotator program

