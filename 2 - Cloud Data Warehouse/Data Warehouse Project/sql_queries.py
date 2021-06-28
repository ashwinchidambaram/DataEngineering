import configparser

#### CALL CONFIG ####################################################################################
#####################################################################################################
'''
Purpose: Call 'configparser' so that we can get the needed values from dwh.cfg

'''
config = configparser.ConfigParser()
config.read('dwh.cfg')

#### DROP TABLES ####################################################################################
#####################################################################################################
'''
Purpose: Drop all tables either before creating DWH or when we want to delete our Redshift cluster

'''

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

#### CREATE TABLES ##################################################################################
#####################################################################################################
'''
Purpose: Create all tables for our DWH

Tables Created:

    - staging_events: staging table to temporarily contain all user events data from JSON files
                        located in AWS S3 buckets
    - staging_songs: staging table to temporarily contain all song data from JSON files located
                        in AWS S3 buckets
    - songplay: table to store aggregated data from both staging tables regarding the user's activity
                        using the Sparkify platform
    - users: table to contain data about the user
    - songs: table to contain data about the songs available on the Sparkify platform
    - artist: table to contain information about the artists
    - time: table to split timestamp parts

'''

staging_events_table_create= ("""

    CREATE TABLE IF NOT EXISTS staging_events(
        staged_events_id int IDENTITY(0,1),
        artist varchar,
        auth varchar,
        first_name varchar,
        gender varchar,
        iteminSession int,
        last_name varchar,
        length float,
        level varchar,
        location varchar,
        method varchar,
        page varchar,
        registration bigint,
        session_id int,
        song varchar,
        status int,
        ts bigint,
        userAgent varchar,
        user_id varchar,
        PRIMARY KEY(staged_events_id))
""")

staging_songs_table_create = ("""

    CREATE TABLE IF NOT EXISTS staging_songs(
        staged_songs_id int IDENTITY(0,1),
        num_songs int,
        artist_id varchar,
        artist_latitude float,
        artist_longitude float,
        artist_location varchar,
        artist_name varchar,
        song_id varchar,
        title varchar,
        duration float,
        year int,
        PRIMARY KEY(staged_songs_id))
""")

songplay_table_create = ("""

    CREATE TABLE IF NOT EXISTS songplay(
        songplay_id int IDENTITY(0,1),
        start_time timestamp NOT NULL,
        user_id varchar NOT NULL,
        level varchar,
        song_id varchar,
        artist_id varchar,
        session_id int,
        location varchar,
        user_agent varchar,
        PRIMARY KEY(songplay_id))
""")

user_table_create = ("""

    CREATE TABLE IF NOT EXISTS users(
        user_id varchar,
        first_name varchar,
        last_name varchar,
        gender varchar,
        level varchar,
        PRIMARY KEY(user_id))
""")

song_table_create = ("""

    CREATE TABLE IF NOT EXISTS songs(
        song_id varchar,
        title varchar,
        artist_id varchar,
        year varchar,
        duration float,
        PRIMARY KEY(song_id))
""")

artist_table_create = ("""

    CREATE TABLE IF NOT EXISTS artist(
        artist_id varchar,
        name varchar,
        location varchar,
        latitude float,
        longitude float,
        PRIMARY KEY(artist_id))
""")

time_table_create = ("""

    CREATE TABLE IF NOT EXISTS time(
        start_time timestamp,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int,
        PRIMARY KEY(start_time))
""")

#### LOAD TO STAGING TABLES #########################################################################
#####################################################################################################
'''
Purpose: Load all our data from S3 buckets to the staging tables so we can load to our production
         tables more easily.

'''

staging_events_copy = ("""

    COPY staging_events FROM '{}'
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    JSON AS '{}'
""").format(config.get('S3', 'LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""

    COPY staging_songs FROM '{}'
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    JSON as 'auto'
""").format(config.get('S3', 'SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

#### LOAD TO FINAL TABLES ###########################################################################
#####################################################################################################
'''
Purpose: Load the data we want from the staging tables into our production tables after
         performing any transforms we need to.

'''

songplay_table_insert = ("""

    INSERT INTO songplay(
        start_time,
        user_id,
        level,
        song_id,
        artist_id,
        session_id,
        location,
        user_agent)
    SELECT timestamp 'epoch' + staging_events.ts/1000 * interval '1 second' as start_time,
        staging_events.user_id,
        staging_events.level,
        staging_songs.song_id,
        staging_songs.artist_id,
        staging_events.session_id,
        staging_events.location,
        staging_events.userAgent
    FROM staging_events
    JOIN staging_songs ON staging_events.song = staging_songs.title
        AND staging_events.artist = staging_songs.artist_name
    WHERE staging_events.page = 'NextSong'
        AND staging_events.user_id IS NOT NULL
""")

user_table_insert = ("""

    INSERT INTO users(
        user_id,
        first_name,
        last_name,
        gender,
        level)
    SELECT user_id, first_name, last_name, gender, level
    FROM staging_events
    WHERE user_id IS NOT NULL
""")

song_table_insert = ("""

    INSERT INTO songs (
        song_id,
        title,
        artist_id,
        year,
        duration)
    SELECT song_id, title, artist_id, year, duration
    FROM staging_songs
    WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""

    INSERT INTO artist (
        artist_id,
        name,
        location,
        latitude,
        longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""

    INSERT INTO time(
        start_time,
        hour,
        day,
        week,
        month,
        year,
        weekday)
    SELECT timestamp 'epoch' + staging_events.ts/1000 * interval '1 second' as start_time,
        extract(hour from start_time) as hour,
        extract(day from start_time) as day,
        extract(week from start_time) as week,
        extract(month from start_time) as month,
        extract(year from start_time) as year,
        extract(weekday from start_time) as weekday
    FROM staging_events
""")

#### QUERY LIST #####################################################################################
#####################################################################################################

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
