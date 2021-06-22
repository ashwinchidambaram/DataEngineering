# Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

# Project Description
In this project, you'll apply what you've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, you will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

# Project Information
=====================

## Project Datasets
The datasets that we will be using for Sparkify reside in S3.

  - Song Data Path - [s3://udacity-dend/song_data]
    - Each song is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

    > song_data/A/B/C/TRABCEI128F424C983.json
    > song_data/A/A/B/TRAABJL12903CDCF1A.json

  - Log Data Path - [s3://udacity-dend/log_data]
    -

  - Log Data JSON Path - [s3://udacity-dend/log_json_path.json]

Song Datasets
