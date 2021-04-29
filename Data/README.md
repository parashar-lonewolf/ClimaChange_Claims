## Table of contents:
* [The Data](#the-data)
* [Data extraction](#data-extraction)
* [Data cleaning](#data-cleaning)

## The Data
*  Articles from New York Times(1987-2007), in the folder "climate"
*  Filtered by "Climate" related articles and further by "Kyoto" as keyword
*  Stored as: 4mFullData_NYT_KyotoConferenceData_cleaned.txt with 4mFullData_Kyoto_filename_list.txt as filename/date index

## Data-extraction
#### After having created the virtual-env and installed the libraries from requirements.txt: 
* To clean the data content ouit of the .xml files of the NYT articles
```
####  Run the data-extractor:
##### May want to change the output file-names, if they already exist
$ python3 [data_extractor_newKyoto.py](./data_extractor_newKyoto.py) 
```
##### Four files will be created:
I.	DATA-FILES:

* [4mFullData_Kyotoclean_data_head.py](./4mFullData_Kyotoclean_data_head.txt)
* [4mFullData_Kyotoclean_data_abstract.py](./4mFullData_Kyotoclean_data_abstract.txt)
* [4mFullData_Kyotoclean_data_content.py](./4mFullData_Kyotoclean_data_content.txt)

II.	INDEX-FILE:

* [4mFullData_Kyoto_filename_list.py](./4mFullData_Kyoto_filename_list.txt)
## Data cleaning
```
#### 2. Run the data cleaner:
##### May want to change source and destination filenames
$ python3 clean_dataset_creator.py

```
##### One file will be created:

* [This](./4mFullData_NYT_KyotoConferenceData_cleaned.txt)
	i.e the final cleaned dataset
After reading from [the xml extracted data](./4mFullData_Kyotoclean_data_content.txt)
and [This](./4mFullData_NYT_KyotoConferenceData_cleaned.txt) will be used by the Annotator.
