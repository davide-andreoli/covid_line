# covid_line: A pipeline for COVID-19 data
This project aims to be a full data pipeline for italian COVID-19 data, starting from the extraction of raw data up to the presentation in form of dashboard. It is built upon docker, allowing anyone to play with it with no (or not much) additional setup.

## What this project is
This project is intended to emulate a data engineerging and analytics pipeline with a rather simple dataset. The approach will try to be as solid as possible, and even though one could argue that some steps are not needed for the final results, I tried to include them for the sake of completness of the process.

## What this project is not
The pipeline works and the data related stuff tries to be as solid as possible, but this project is not intended to be a fully production ready development, especially in the DevOps realm. The configuration of the various tools used is done in order to make them work, not to make them secure or production ready, so keep this in mind while you explore.

# Tools
As for tools, I chose to use only Apache tools, for different reasons:
- most of them are really solid tools used in different production environments
- I don't usually use them in my daily work, as I am working with different technologies
- they are open source

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
The data is then read from the month folders and grouped into daily parquet files, partitioned by country code and stored in the pq folder, with the following folder structure.
```
Pq folder
|    
└-- Year folder  
    |    
    └-- Month folder
        |    
        └-- Day folder
            |    
            └-- cases_date.parquet
```
One could argue that with such a dataset this step is useless, and would probably be right. However, keeping in mind the scope of the project, this step effectively emulates the loading of the data in a data lake, storing it efficiently for further queries.

As of right now the maximum granularity is chosen, in order to easily reload onde day's data when needed. This is done becuase the same pipeline could be adapted to different datasets with few modifcations (e.g.: retail transactions). For the current exampole, as the data is very limited, and would be very limited even if all the countries were to be included, the convenience gain is minimal, but still I prefer this kind of design.

This folder structure will be kept even for future data (for example: vaccination).

### Data warehousing
In order to support different analytical tasks and SQL-like queries, raw data is stored inside Hive.
The data is loaded into a "cases" table, overwriting data for the same date but leaving all the rest of the table untouched.
The table structure is very simple, and can be seen below.
| column_name | data_type | description |
| --- | --- | --- |
| collection_date | date | The date to which the measurement refers to. |
| collection_id | string | The collection id, it is an hash of the concatenation of the country_cod and the collection_date |
| country_cod | string | The country code to which the measurement refers to. |
| new_positive_cases | int | The number of positive cases for the day. |

### Data visualization
The data visualization tool of choice is Apache Superset, which is connected directly to the Hive Database.
Dashboards can be defined as YAML files and later imported through the CLI, or even better created using the UI, exported and then imported back the next time the container will start.
All the files can be found under:
docker_entrypoints
|    
└-- superset  
    |    
    └-- dashboard/database_export
The GUI can be accessed at http://localhost:8088/