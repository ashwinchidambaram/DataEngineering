# Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

# Project Description
In this project, you'll apply what you've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, you will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

# Project Information

## Project Datasets
The datasets that we will be using for Sparkify reside in S3.

  - Song Dataset Path - [s3://udacity-dend/song_data]
    - Each song is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

      - *song_data/A/B/C/TRABCEI128F424C983.json*
      - *song_data/A/A/B/TRAABJL12903CDCF1A.json*

    - The song file (*TRAABJL12903CDCF1A.json*) looks like:
      > {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

  - Log Dataset Path - [s3://udacity-dend/log_data]
    - Contains simulated app activity logs based on above data. The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in the dataset:

      - *log_data/2018/11/2018-11-12-events.json*
      - *log_data/2018/11/2018-11-13-events.json*

    - The log file (*2018-11-12-events.json*) looks like:

      ![](https://video.udacity-data.com/topher/2019/February/5c6c3ce5_log-data/log-data.png)

  - Log Dataset JSON Path - [s3://udacity-dend/log_json_path.json]

## Schema for Song Play Analysis
- Fact Table
  1. **songplays** -  records in event data associated with song plays i.e. records with page *NextSong*
      > *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

- Dimension Tables:
  2. **users** - users in the app
      > *user_id, first_name, last_name, gender, level*

  3. **songs** - songs in music database
      > *song_id, title, artist_id, year, duration*

  4. **artists** - artists in music database
      > *artist_id, name, location, latitude, longitude*

  5. **time** - timestamps of records in **songplays** broken down into specific units
      > *start_time, hour, day, week, month, year, weekday*
