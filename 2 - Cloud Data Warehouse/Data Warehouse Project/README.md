# **Data Warehouse - Sparkify**
## *Author: Ashwin Chidambaram*

### **Files Included:**
- *create_table.py*
  - Where I will create the fact and dimension tables for the star schema in Redshift.
- *etl.py*
  - Where I will load data from S3 into staging tables on Redshift and then process that data into my analytics tables on Redshift.
- *sql_queries.py*
  -  Where I will define the SQL statements, which will be imported into the two other files above.
- *README.md*
  - Where I will discuss the contents of this project, my process to tackle this project, and the decisions I made for the ETL pipeline.

-------------------------------------------------------------------------------

# **Project Information**

## Introduction
*A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.*

*As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.*

## Project Description / How I Contributed
In this project, I have applied what I've learned about data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. I will be loading data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

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
  1. **users** - users in the app
      > *user_id, first_name, last_name, gender, level*

  1. **songs** - songs in music database
      > *song_id, title, artist_id, year, duration*

  1. **artists** - artists in music database
      > *artist_id, name, location, latitude, longitude*

  1. **time** - timestamps of records in **songplays** broken down into specific units
      > *start_time, hour, day, week, month, year, weekday*

- Staging Tables:
  1. **staging_events** - users in the app
      > *staged_events_id, artist, auth, first_name, gender, iteminSession, last_name, length, level, location, method, page, registration, session_id, song, status, ts, userAgent, user_id*

  1. **staging_songs** - users in the app
      > *staged_songs_id, num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year*

# **Project Process**
1. Create Table Schemas
    1.  First, I will be designing the schemas for both the fact and dimension tables according to the specifications provided for this project.
    2. Next, I will write CREATE statements for each of the tables within the file *sql_queries.py*.
    3. After that, I will write the logic required to connect to the database within *create_tables.py* and include logic to create all of Sparkify's tables using the queries I wrote in  *sql_queries.py*.
    4. Following that, I will create the IAM role that has read access to S3 and store the credentials to a secure file to be called within *create_tables.py*.

2. Build ETL Pipeline
    1. First, I will implement the logic to load data from S3 to staging tables within Redshift.
    2. Following which, I will load data from the staging tables to the analytics tables in Redshift.

# **Project Results**


# **Project Discussion**
### 1. Purpose of Database within context Sparkify, and their Analytical Goals:
1. Discuss the purpose of this database in context of the startup, Sparkify, and their analytical goals.

### 2. Justification of Database Schema Design and ETL Pipeline:
2. State and justify your database schema design and ETL pipeline.

### 3. Example Queries and Results:
3. Provide example queries and results for song play analysis.

    1. Check [**staging_events**] table
        > QUERY:
        >> *SELECT \* FROM staging_events LIMIT 5*

        ![](/Data Warehouse Project/Query_Results/staging_events_queryresults.png)

    2. Check [**staging_songs**] table
        > QUERY:
        >> *SELECT \* FROM staging_songs LIMIT 5*

        ![](/assets/images/philly-magic-gardens.jpg)

    3. Check [**songplay**] table
        > QUERY:
        >> *SELECT \* FROM songplay LIMIT 5*

        ![](/assets/images/philly-magic-gardens.jpg)

    4. Check [**users**] table
        > QUERY:
        >> *SELECT \* FROM users LIMIT 5*

        ![](/assets/images/philly-magic-gardens.jpg)

    5. Check [**songs**] table
        > QUERY:
        >> *SELECT \* FROM songs LIMIT 5*

        ![](/assets/images/philly-magic-gardens.jpg)

    6. Check [**artist**] table
        > QUERY:
        >> *SELECT \* FROM artist LIMIT 5*

        ![](/assets/images/philly-magic-gardens.jpg)

    7. Check [**time**] table
        > QUERY:
        >> *SELECT \* FROM time LIMIT 5*

        ![](/assets/images/philly-magic-gardens.jpg)



## OTHER STUFF ##################
Staging tables:
- Staging tables are tables containing your business data in some form or other and helps in preparing your business data, usually taken from some business application. They are temporary table containing the business data.

- Staging tables act a reservoir where the data is stored and after further processing it is moved to fact and dimension tables

- Most traditional ETL processes perform their loads using three distinct and serial processes: extraction, followed by transformation, and finally a load to the destination. However, for some large or complex loads, using ETL staging tables can make for better performance and less complexity.

- Staging tables are normally considered volatile tables, meaning that they are emptied and reloaded each time without persisting the results from one execution to the next. Staging tables should be used only for interim results and not for permanent storage.

- This load design pattern has more steps than the traditional ETL process, but it also brings additional flexibility as well. By loading the data first into staging tables, you’ll be able to use the database engine for things that it already does well. For example, joining two sets of data together for validation or lookup purposes can be done in most every ETL tool, but this is the type of task that the database engine does exceptionally well.

====================

- PROJECT: In this project and as part of the specification, we should consider using a staging table on the destination database as a means for processing interim data results.

- PROJECT
1.) Delete existing data in the staging table(s)
2.) Extract the data from the source
3.) Load this source data into the staging table(s)
4.) Perform relational updates (SQL) to cleanse or apply business rules to the data, repeating this transformation stage as necessary
5.) Load the transformed data from the staging table(s) into the final destination table(s)

- You may also utilize JOIN statements on both staging tables to insert data into the songplays table, by using staging_events and staging_songs

  FROM staging_events
  JOIN  staging_songs
  ON

- So, In sqlqueries.py, you need to:

1. Define the tables for staging tables(2 tables, staging_events_table,staging_songs_table)
2. Define the start schema tables, songsplay(Fact able) and time, artists, users, songs(dimension tables)
3. Use copy statement to copy the log_data and song_data files to your redshift staging tables you created above.
4. Once the data is loaded in the staging tables, use the staging tables to load the data in fact and dimension tables, (project 1 as a reference)





https://knowledge.udacity.com/questions/505535
https://knowledge.udacity.com/questions/148404
https://knowledge.udacity.com/questions/400479
