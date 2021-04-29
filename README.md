## Table of contents
* [Intro & installation](#introduction)
* [The Data](./Data)
* [The Annotator](#the-annotator)
* [The Tagger](#the-tagger)
* [Claim classification](#claim-classification)
* [Political Discourse network](#political-discourse-network)

## Introduction
#### For Linux/Ubuntu based systems:
##### Objective: 
* To tag and model ACTOR(any Person/Organisation) and their corresponding CLAIM(S) made on environmental issues, emmisions and/or climate-change and whether they support the claim or not
```
#### 1. Install python virtualenv:
$ pip install virtualenv 

#### 2a. Create a virtual environment
$ virtualenv climachange_env
## OR
$ python3 -m virtualenv climachange_env 

#### 2b. Add virtual emvironment to jupyter-notebook (for using the .ipynb notebooks)
$ python3 -m ipykernel install --user --name=climachange_env  

#### 3. Activate virtual environment
$ source climachange_env/bin/activate

#### 4. Create git clone repo
$ git clone https://github.com/parashar-lonewolf/ClimaChange_Claims.git

#### 5. Move to folder
$ cd ClimaChange_Claims

#### 6. Install requirements
$ pip install -r requirements.txt 

#### 7. Run Annotator
$ python3  ACTOR_CLAIM_ANNOTATOR.py 
```
### The annotator
#### Instructions for using the Annotator :
* All tagged data will be stored in ConLL format as: ConLLformat_annotator.txt (here you see ConLLformat_annotator_ank/ian.txt to indicate the individual annotaions hence performed)
* All claims will be stored in [Save](./Save) folder (here you see Claims_ank/ian.txt to indicate the individual annotaions hence we have performed)

##### The first window will have ask
##### Window 1. 
"'So do you think this has a CLAIM ?'

1. You answer yes by selecting a new actor and/or just clicking "Next"
![Window 1](https://cdn.mathpix.com/snip/images/GgCijP3eYTY7_q9RZ9wDhaQPLMIe_LbUcv0Q5JRYbSw.original.fullsize.png)
##### Window 2
'Select the Claim boundaries'

2. This brings us to the claim annotations, where we have to select the words to be used as boundaries, i.e
the first word and the last word of the claim sequence.
For eg: A recent study in the journal Nature  confirmed that the freezing levels in the mountains have indeed 
shifted upward about 500 feet since 1970, representing a warming of close to 2 Fahrenheit.
you select [that] and [Fahrenheit.] on the window. Choose a Polarity for the Claim ('+'/[Helping],'-'/[Ignoring] and '0'/[Neutral]) and click on "Next"
![Window 2](https://cdn.mathpix.com/snip/images/NX-nirTfLllMaPCywMVH93gqh53jMRSyf45YE-qBMpM.original.fullsize.png)

3. if you select "Cancel" at WINDOW 1, you remove that sentence from tagging criterias.
4. if you select "Exit" the prgram ends and only writes till last completely tagged article
5. If you select save, it will save all current progress of dataset annotations,
and once you exit and restart, the annotation will continue from the last annotation point.
6. In case, you made a mistake in the annotation, the current version addresses the issue as:

*click on "Save Prev Annotations"*

*press "Exit"*

*rerun the annotator program*

##### ConLL format used: (Using above output as example)
![ConLL data](https://cdn.mathpix.com/snip/images/hv_6zy1J3ANUcGHwn-f19cxGhGVAexgNxZuy4uEe8-k.original.fullsize.png)

### The tagger
##### There are two implementations of creating a language model to predict and output our custom tags:
* [Notebook with CRF tagger train/test with and without claim classification](./CRF_ActorClaim_tagger.ipynb)      

Each of these notebooks have a functional tagger mdoel made using CRF, the model files are also available for use using the same pre-processing as done in the notebook

### Claim classification
All the tagged Claims are classified into 5 clusters using K-means:
* [k-means clusering of claims](./KMeans_Claim_Custering.ipynb)
* The output is beautifully portrayed below (also check https://claimclusters.tiiny.site/)

![Claim Cluster](./download.png)

### Political discourse network

* This notebook uses 'jgraph' to create political discourse:
[ Political discourse network over time](./Political_Discourse_networks.ipynb)
