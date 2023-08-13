# covid_line: A pipeline for COVID-19 data
This project aims to be a full data pipeline for italian COVID-19 data, starting from the extraction of raw data up to the presentation in form of dashboard. It is built upon docker, allowing anyone to play with it with no (or not much) additional setup.

## What this project is
This project is intended to emulate a data engineerging and analytics pipeline with a rather simple dataset. The approach will try to be as solid as possible, and even though one could argue that some steps are not needed for the final results, I tried to include them for the sake of completness of the process.

## What this project is not
Even though the pipeline works and the data related stuff tries to be as solid as possible, this project is not intended to be a fully production ready development, especially in the DevOps realm. The configuration of the various tools used is done in order to make them work, not to make them secure or production ready, so keep this in mind while you explore.

# Architecture
In this section I will go throught the architecture of the pipeline, starting from the general overview and then going into more details.
## Overview
The raw data is extracted daily from the Protezione Civile's github repository, and stored in a raw folder, from which it is extracted, grouped into months and converted to parquet files.

### Data extraction
The data comes directly from the Protezione Civile's [Github Repository](https://github.com/pcm-dpc/COVID-19). They host a summary file containing all data directly, but since the aim of the project is to emulate a production pipeline as much as possible, I decided to extract the data from the daily uploads, even though this means that the data is really small as each file contains only one line.
The pipeline is built to be ready to be expanded with other countries' data in the future.

### Data loading
The data is stored as raw csv files in the raw folder, with the following folder structure.
```
Raw folder
|    
└-- Year folder  
    |    
    └-- Month folder
        |    
        └-- Day folder
            |
            └-- countrycode_cases_date.csv  
```
The data is then read from the month folders and grouped into monthly parquet files, partitioned by date and stored in the pq folder, with the following folder structure.
```
Pq folder
|    
└-- Year folder  
    |    
    └-- Month folder
        |    
        └-- Day folder
            |    
            └-- cases.parquet
```
One could argue that with such a dataset this step is useless, and would probably be right. However, keeping in mind the scope of the project, this step effectively emulates the loading of the data in a data lake, storing it efficiently for further queries.

I decided to group it by month partly because of its size, partly because it often makes sense to reason by month in this cases (even though by year makes probably even more sens). I am still evaluating other lake's designs.