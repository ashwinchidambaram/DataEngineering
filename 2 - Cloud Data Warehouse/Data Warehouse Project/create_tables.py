# Import necessary Python packages
import configparser
import psycopg2
import boto3
import json
import pandas as pd
import time

# Import functions for creating and dropping tables from sql_queries.py
from sql_queries import create_table_queries, drop_table_queries

#### DROP & CREATE TABLE METHODS ####################################################################
#####################################################################################################

# Purpose: Drop tables if they exist
def drop_tables(cur, conn):

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

    # ~~~~ DEBUG ~~~~ Check if tables have been successfully dropped
    debugMode(8)

# Purpose: Create tables
def create_tables(cur, conn):

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

        # ~~~~ DEBUG ~~~~ Check if tables have been successfully created
        debugMode(9)

#### DEBUGGING METHOD ###############################################################################
#####################################################################################################

# Purpose: Track progress through script, and ensure that individual parts are executing correctly
def debugMode(a):

    if mode == True:

        if a == 1: # Line: 142
            print("createRedshiftCluster(): Pulling of DWH Parameters was performed successfully")

        elif a == 2: # Line: 153
             print("createRedshiftCluster(): All clients were successfully created.")

        elif a == 3: # Line: 185
            print("createRedshiftCluster(): IAM Role creation performed successfully.")

        elif a == 4: # Line: 211
            checkClusterStatus()
            print("\n")

        elif a == 5: # Line: 217
            checkClusterStatus()
            print("\n")

        elif a == 6: # Line: 223
            print("Connection Details: ")
            print(connValues)

        elif a == 7: # Line: 296
            print("deleteRedshiftCluster(): IAM Role deletion performed successfully.")

        elif a == 8: # Line: 23
            print("drop_tables(): Tables dropped successfully.")

        elif a == 9: # Line: 33
            print("create_tables(): Tables created successfully.")

    else:
        pass


##### REDSHIFT CLUSTER CREATION & DELETION METHODS ##################################################
#####################################################################################################

def createRedshiftCluster():
    '''
    Purpose: Create a Redshift cluster

    Parts of this Method:

        - DWH Parameters:
            -- Will load the DWH parameters I set within dwh.cfg so that we can create
                a data warehouse according to the client's specifications.

        - Client Creation:
            -- Creates the clients that are required to utilize  both s3 and Redshift,
                and will also create the IAM client to interact with Redshift

        - IAM Role Creation:
            -- Actually creates the IAM Role and attaches the policy key needed to
                interact with Redshift

        - Redshift Cluster Creation
            -- Actually creates the Redshift cluster using values from the DWH parameters

    Debugging Values Included:

        - debugMode(1) : Prints if parameter creation is successful
        - debugMode(2) : Prints if client creation is successful
        - debugMode(3) : Prints if IAM role creation is successful
        - debugMode(4) : Checks if redshift cluster is being created

    '''
    #################################
    #### Define global variables ####
    #################################
    global redshift                    # Used across the script to access the redshift cluster
    global DWH_CLUSTER_IDENTIFIER      # Used to identify the DWH Cluster
    global iam                         # Used to identify the IAM role
    global DWH_IAM_ROLE_NAME
    global PolicyArn

    #### DWH Parameters ####################################################################
    ## Load the Data Warehouse Parameters we set in dwh.cfg to create a Redshift database ##
    ########################################################################################
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    KEY                    = config.get('AWS','KEY')
    SECRET                 = config.get('AWS','SECRET')

    DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
    DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
    DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")

    DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
    DWH_DB                 = config.get("DWH","DWH_DB")
    DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
    DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
    DWH_PORT               = config.get("DWH","DWH_PORT")

    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")

    (DWH_DB_USER, DWH_DB_PASSWORD, DWH_DB)

    # ~~~~ DEBUG ~~~~ Print if parameter creation is successful
    debugMode(1)

    #### Client Creation #############################################
    ## Create the Clients required to interact with s3 and Redshift ##
    ##################################################################

    s3 = boto3.resource('s3', region_name = "us-west-2", aws_access_key_id = KEY, aws_secret_access_key = SECRET)
    iam = boto3.client('iam', region_name = "us-west-2", aws_access_key_id = KEY, aws_secret_access_key = SECRET)
    redshift = boto3.client('redshift', region_name = "us-west-2", aws_access_key_id = KEY, aws_secret_access_key = SECRET)

    # ~~~~ DEBUG ~~~~ Print if client creation is successful
    debugMode(2)

    #### IAM Role Creation ############################
    ## Create the IAM Role and attach the policy key ##
    ###################################################
    try:
        dwhRole = iam.create_role(
            Path = '/',
            RoleName = DWH_IAM_ROLE_NAME,
            Description = "Allows Redshift clusters to call AWS services on our behalf.",
            AssumeRolePolicyDocument = json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                                'Effect': 'Allow',
                                'Principal': {'Service': 'redshift.amazonaws.com'}}],
                    'Version': '2012-10-17'
                }
            )
        )

    except Exception as e:
        print("Error with IAM Role Creation: {}".format(e))

    # Attach Policy Key
    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                       PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                      )['ResponseMetadata']['HTTPStatusCode']

    # Get IAM Role ARN
    roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']
    print('RoleARN: {}'.format(roleArn))

    # ~~~~ DEBUG ~~~~ Print if IAM role creation is successful
    debugMode(3)

    #### Redshift Cluster Creation ###################################
    ## Create the Redshift cluster using segments/values from above ##
    ##################################################################
    try:
        response = redshift.create_cluster(
            # Add hardware parameters according to DWH Parameters in config file
            ClusterType = DWH_CLUSTER_TYPE,
            NodeType = DWH_NODE_TYPE,
            NumberOfNodes = int(DWH_NUM_NODES),

            # Add parameters for identifiers & credentials according to DWH Parameters in config file
            DBName = DWH_DB,
            ClusterIdentifier = DWH_CLUSTER_IDENTIFIER,
            MasterUsername = DWH_DB_USER,
            MasterUserPassword = DWH_DB_PASSWORD,

            # Add parameter for role to allow s3 access
            IamRoles = [roleArn]
        )

    except Exception as e:
        print("Error with creating Redshift Cluster: {}".format(e))

    # ~~~~ DEBUG ~~~~ Check if redshift cluster is being created
    debugMode(4)

def deleteRedshiftCluster():
    redshift.delete_cluster(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER, SkipFinalClusterSnapshot=True)

    # ~~~~ DEBUG ~~~~ Check if redshift cluster is being deleted
    debugMode(5)

    iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)

    # ~~~~ DEBUG ~~~~ Print if IAM role deletion is successful
    debugMode(7)

##### CLUSTER STATUS CHECK METHOD ###################################################################
#####################################################################################################

# Purpose: Check and give the status of the cluster
def checkClusterStatus():

    # Used to determine whether to "activate" the debug mode
    status = False

    # Used to determine whether the cluster is in the process of being created or deleted
    waiting = False

    while status != True:
        try:
            myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER, TagKeys=['ClusterStatus'])['Clusters'][0]
            clusterStatus = myClusterProps['ClusterStatus']

            if clusterStatus == 'available':
                print ("CLUSTER STATUS: Cluster is available")
                status = True
                waiting = False

            elif ((clusterStatus == 'creating') and (waiting == False)):
                print ("CLUSTER STATUS: Cluster is being created...")
                status = False
                waiting = True

            elif ((clusterStatus == 'deleting') and (waiting == False)):
                print ("CLUSTER STATUS: Cluster is being deleted...")
                status = False
                waiting = True

            elif waiting == True:
                print("...")
                time.sleep(10)

        except:
            status = True
            print("CLUSTER STATUS: There is no active Redshift cluster.")

#####################################################################################################
#### MAIN METHOD ####################################################################################
#####################################################################################################

def main():

    #################################
    #### Define global variables ####
    #################################
    global mode                        # Used to determine whether to run in debug mode
    global connValues                  # Used to debug the connection details of DB

    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    print("Would you like to turn debug mode on (Y/N)?")
    x = input()
    print("\n")
    if x == 'Y' or x == 'y':
        mode = True
    else:
        mode = False

    # Create the Redshift cluster
    createRedshiftCluster()
    #time.sleep(30)

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    connValues = ("   host={} \n   dbname={} \n   user={} \n   password={} \n   port={}".format(*config['CLUSTER'].values()))

    # ~~~~ DEBUG ~~~~ Get connection details
    debugMode(6)
    cur = conn.cursor()

    #create_schema(cur, conn)
    drop_tables(cur, conn)
    create_tables(cur, conn)

    # Delete the Redshift cluster
    print("Would you like to delete the cluster (Y/N)?")
    x = input()
    print("\n")
    if x == 'Y' or x == 'y':
        deleteRedshiftCluster()
    else:
        pass

    conn.close()


if __name__ == "__main__":
    main()
