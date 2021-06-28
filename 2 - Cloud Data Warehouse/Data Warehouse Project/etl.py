import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
from create_tables import createRedshiftCluster, deleteRedshiftCluster

#### LOAD TO TABLES METHODS #########################################################################
#####################################################################################################

# Load data to staging tables
def load_staging_tables(cur, conn):

    # ~~~~ DEBUG ~~~~ Notify when about to load data to staging tables
    debugMode(1)

    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

        # ~~~~ DEBUG ~~~~ Notify when data has been loaded to respective staging tables
        debugMode(2)

# Load data to all production tables
def insert_tables(cur, conn):

    # ~~~~ DEBUG ~~~~ Notify when about to load data to production tables
    debugMode(3)

    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

        # ~~~~ DEBUG ~~~~ Notify when data has been loaded to respective production tables
        debugMode(4)

#### DEBUGGING METHOD ###############################################################################
#####################################################################################################

# Purpose: Track progress through script, and ensure that individual parts are executing correctly
def debugMode(a):

    if mode == True:

        if a == 1: # Line: 13
            print("\nPreparing to load data into staging tables:")

        elif a == 2: # Line: 20

            i = 2

            if i == 1:
                print("====> log_data has been loaded to staging table")

            else:
                print("====> song_data has been loaded to staging table")

            i = i + 1

        elif a == 3: # Line: 26
            print("\nPreparing to load data into [songplay, user, song, artist, time] tables:")

        elif a == 4: # Line: 33

            i = 1

            if i == 1:
                print("====> data has been loaded to [songplay] table")

            elif i == 2:
                print("====> data has been loaded to [user] table")

            elif i == 3:
                print("====> data has been loaded to [song] table")

            elif i == 4:
                print("====> data has been loaded to [artist] table")

            elif i == 5:
                print("====> data has been loaded to [time] table")

            i = i + 1

    else:
        pass

#####################################################################################################
#### MAIN METHOD ####################################################################################
#####################################################################################################
def main():

    global mode

    print("Would you like to turn debug mode on (Y/N)?")
    x = input()
    if x == 'Y' or x == 'y':
        mode = True
    else:
        mode = False

    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)

    insert_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
