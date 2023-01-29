# covid_line: A pipeline for COVID-19 data
This project aims to be a full data pipeline for italian COVID-19 data, starting from the extraction of raw data up to the presentation in form of dashboard. It is built upon docker, allowing anyone to play with it with no (or not much) additional setup.

## What this project is
This project is intended to emulate a data engineerging and analytics pipeline with a rather simple dataset. The approach will try to be as solid as possible, and even though one could argue that some steps are not needed for the final results, I tried to include them for the sake of completness of the process.

## What this project isn'
Even though the pipeline works and the data related stuff tries to be as solid as possible, this project is not intended to be a fully production ready development, especially in the DevOps realm. The configuration of the various tools used is done in order to make them work, not to make them secure or production ready, so keep this in mind while you explore.

# Architecture
In this section I will go throught the architecture of the pipeline, starting from the general overview and then going into more details.
## Overview
The raw data is extracted daily from the Protezione Civile's github repository, and stored in a raw folder