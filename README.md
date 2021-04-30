## Table of contents
* [Intro & installation](#introduction)
* [The Data](./Data)
* [The Annotator](#the-annotator)
* [Claim classification](#claim-classification)
* [The Tagger](#the-tagger)
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
## The annotator
#### Instructions for using the Annotator :
* All tagged data will be stored in ConLL format as: ConLLformat_annotator.txt (here you see ConLLformat_annotator_ank/ian.txt)
* All claims will be stored in [Save](./Save) folder (here you see Claims_ank/ian.txt)

#### The GUI windows 
##### To explain how this works, As an example lets talk about a claim made by Bill Clinton from the NYT article from 1997/06/23 (this is stored  in Claims.txt which is the [Save](./Save) folder)

" *But in a sharp dispute with France and other European nations that dominated this morning's final session of ''The Summit of the Eight,'' President Clinton refused to commit the United States to a specific reduction in the emission of carbon dioxide and the other greenhouse gases that contribute to global warming, agreeing only to ''substantial reductions'' by 2010.* "
                                                    
### 1. 
"'So do you think this has a CLAIM ?'

You answer yes by selecting a new actor, here *President* and *Clinton* and clicking **Next** (if the annnotator has already correctly chosen the actor for you, you may just click **Next**)

![Window 1](https://cdn.mathpix.com/snip/images/ZZowOn83cgaEXQMdBZ3ldzLU1er468JAs8wn5TDehmY.original.fullsize.png)

### 2.
'Select the Claim boundaries'

This brings us to the claim annotations, where we have to select the words to be used as boundaries, i.e
the first word and the last word of the claim sequence. You can select *commit* and *warming,* on the window. Choose if the actor **Supports** or is **Against** the claim (in this case since he ' "refused" to commit ', it's **Against**) and click on **Next**

![Window 2](https://cdn.mathpix.com/snip/images/wO2YY4boghyZ-UNffZ6GdqktjmRMKEEdpYI9RYdah_E.original.fullsize.png)

3. if you select **Cancel** at WINDOW 1, you remove that sentence from tagging criterias.
4. if you select **Exit** the prgram ends and, when restarted, it restarts at the candidate sentence quit, so progress is autosaved by default.
5. If you select save, it will save all current progress of dataset annotations in the [Save](./Save) folder as Progress_Manager.txt(saved here as Progress_Manager_ank/ian.txt),
and once you exit and restart, the annotation will continue from the last annotation point.
6. In case, you made a mistake in the annotation, the current version addresses the issue as:
    * click on **Save Prev Annotations***
    * press **Exit***
    * rerun the annotator program*

##### ConLL format used: (Using above output as example)
![ConLL data](https://cdn.mathpix.com/snip/images/ISh58Vf9Pjm1wCk7pLkf3iJZJ7GNBoREzK1GpfNsMBs.original.fullsize.png)

## Claim classification
All the tagged Claims are classified into 5 clusters using K-means:
* [k-means clusering of claims](./KMeans_Claim_Custering.ipynb)
* The output is beautifully portrayed below (also check https://claimclusters.tiiny.site/)

![Claim Cluster](./download.png)

## The tagger
##### There are two implementations of creating a language model to predict and output our custom tags:
* [Notebook with CRF tagger train/test with and without claim classification](./CRF_ActorClaim_tagger.ipynb)      

This notebook has a functional models made using CRF, the model files are also available for use in [Pickles](./Pickles) folder.
We have trained 3 models each of clustered and unclustered data and run them for 500,1000 and 1500 iterations respectively



## Political discourse network

* This notebook uses 'jgraph' to create political discourse:
[ Political discourse network over time](./Political_Discourse_networks.ipynb)
