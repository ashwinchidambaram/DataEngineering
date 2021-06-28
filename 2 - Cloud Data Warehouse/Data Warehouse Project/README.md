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
### 1. Purpose of Database within Context of Sparkify, and their Analytical Goals:

The fictional music streaming platform Sparkify is constantly collecting large quantities of data from their users however have no analytical capabilities since the data is simply stored off in JSON files that can not be easily accessed or queried. By creating this database, it allows Sparkify to have easy access to all their data and will allow them to use it for any of their business needs.

As per the client's request we are using AWS to store their raw data in S3 buckets and warehouse it in Redshift. This ensures data availability across most geographic regions and none of the expensive costs associated with upkeep of local, on-premise servers.

Their analytic goals are not defined, but using the tables created, they will be easily query the data required to answer any of their business needs.

### 2. Justification of Database Schema Design and ETL Pipeline:
2. State and justify your database schema design and ETL pipeline.



### 3. Example Queries and Results:
3. Provide example queries and results for song play analysis.

    1. Check [**staging_events**] table
        > QUERY:
        >> *SELECT \* FROM staging_events LIMIT 5*

        ![](https://raw.githubusercontent.com/ashwinchidambaram/DataEngineering/main/2%20-%20Cloud%20Data%20Warehouse/Data%20Warehouse%20Project/Query_Results/staging_events_queryresults.png)

    2. Check [**staging_songs**] table
        > QUERY:
        >> *SELECT \* FROM staging_songs LIMIT 5*

        ![](https://raw.githubusercontent.com/ashwinchidambaram/DataEngineering/main/2%20-%20Cloud%20Data%20Warehouse/Data%20Warehouse%20Project/Query_Results/staging_songs_queryresults.png)

    3. Check [**songplay**] table
        > QUERY:
        >> *SELECT \* FROM songplay LIMIT 5*

        ![](https://raw.githubusercontent.com/ashwinchidambaram/DataEngineering/main/2%20-%20Cloud%20Data%20Warehouse/Data%20Warehouse%20Project/Query_Results/songplay_queryresults.png)

    4. Check [**users**] table
        > QUERY:
        >> *SELECT \* FROM users LIMIT 5*

        ![](https://raw.githubusercontent.com/ashwinchidambaram/DataEngineering/main/2%20-%20Cloud%20Data%20Warehouse/Data%20Warehouse%20Project/Query_Results/user_queryresults.png)

    5. Check [**songs**] table
        > QUERY:
        >> *SELECT \* FROM songs LIMIT 5*

        ![](https://raw.githubusercontent.com/ashwinchidambaram/DataEngineering/main/2%20-%20Cloud%20Data%20Warehouse/Data%20Warehouse%20Project/Query_Results/song_queryresults.png)

    6. Check [**artist**] table
        > QUERY:
        >> *SELECT \* FROM artist LIMIT 5*

        ![](https://raw.githubusercontent.com/ashwinchidambaram/DataEngineering/main/2%20-%20Cloud%20Data%20Warehouse/Data%20Warehouse%20Project/Query_Results/artist_queryresults.png)

    7. Check [**time**] table
        > QUERY:
        >> *SELECT \* FROM time LIMIT 5*

        ![](https://raw.githubusercontent.com/ashwinchidambaram/DataEngineering/main/2%20-%20Cloud%20Data%20Warehouse/Data%20Warehouse%20Project/Query_Results/time_queryresults.png)
        ![]()
