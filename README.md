## For Linux/Ubuntu based systems:
### 1. Install python virtualenv:
pip install virtualenv

### 2. Create a virtual environment
virtualenv climachange_env

### 3. Activate virtual environment
source climachange_env/bin/activate

### 4. Create git clone repo
git clone https://github.com/parashar-lonewolf/ClimaChange_Claims.git

### 5. Move to folder
cd ClimaChange_Claims

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
![Window 1](https://cdn.mathpix.com/snip/images/l84NuUtIWpOn2dMH854MHh8kTqtPhRJpxBjx91VuFH8.original.fullsize.png)

### WINDOW 2
'Select the Claim boundaries'

2. This brings us to the claim annotations, where we have to select the words to be used as boundaries, i.e
the first word and the last word of the claim sequence.
For eg: A recent study in the journal Nature  confirmed that the freezing levels in the mountains have indeed 
shifted upward about 500 feet since 1970, representing a warming of close to 2 Fahrenheit.
you select [that] and [Fahrenheit.] on the window. choose  POLrity for the Claim and click on "Next"
![Window 2](https://cdn.mathpix.com/snip/images/-Io3tJ3axVg6pUSTEb_GLIMlE5oiangjQH3OjU9hwao.original.fullsize.png)

3. if you select "Cancel" at WINDOW 1, you remove that sentence from tagging criterias.
4. if you select "Exit" the prgram ends and only writes till last completely tagged article
5. If you select save, it will save all current progress of dataset annotations,
and once you exit and restart, the annotation will continue from the last annotation point.
6. In case, you made a mistake in the annotation, the current version addresses the issue as:

*click on "Save Prev Annotations"*

*press "Exit"*

*rerun the annotator program*

### ConLL format used: (Using above output as example)
![ConLL data](https://cdn.mathpix.com/snip/images/5U9XJFTm65qNzJSjBs-GODAAdsxy2AcHUX-77qxJoIc.original.fullsize.png)

