import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
    Function Purpose: Open and process data from song data file to insert into {songs, artists} table

    Inputs:
        - filepath: the filepath where the JSON song data file is stored
        - cur: cursor

    Outputs:
        - 'song_data': Insert [song_id, title, artist_id, year, duration]
                    ==> into songs table
        - 'artist_data': Insert [artist_id, name, location, latitude, longitude]
                    ==> into artists table
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.values[0][[7, 8, 0, 9, 5]].tolist()
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df.values[0][[0, 4, 2, 1, 3]].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Function Purpose: Open and process data from log data file to insert into {time, users, songplays} table

    Inputs:
        - filepath: the filepath where the JSON log data file is stored
        - cur: cursor

    Outputs:
        - time row: Insert [start_time, hour, day, week, month, year, weekday]
                    ==> into time table
        - user row: Insert [user_id, first_name, last_name, gender, level]
                    ==> into artists table
        - 'songplay_data': Insert [start_time, user_id, level, song_id, artist_id, session_id, location, user_agent]
                    ==> into songplays table
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    ####### time table insert #####################
    # convert timestamp column to datetime
    t = df['ts']

    # Create list item
    time_data = []

    # Convert timestamp to (ms)
    for item in t:
        time = pd.Timestamp(ts_input = item, unit = 'ms')
        time_data.append([time, time.hour, time.day, time.weekofyear, time.month, time.year, time.weekday()])

    # insert time data records
    column_labels = column_labels = ('ts','hour', 'day', 'weekofyear', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(time_data, columns = column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    ####### user table insert #####################
    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    ####### songplays table insert ################
    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (time, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
