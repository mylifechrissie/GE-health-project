{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 AndaleMono;}
{\colortbl;\red255\green255\blue255;\red106\green120\blue135;\red38\green38\blue38;\red26\green125\blue169;
\red77\green80\blue81;\red41\green142\blue11;\red148\green108\blue71;\red255\green255\blue255;\red187\green24\blue34;
}
{\*\expandedcolortbl;;\cssrgb\c49020\c54510\c60000;\cssrgb\c20000\c20000\c20000;\cssrgb\c9804\c56471\c72157;
\cssrgb\c37255\c38824\c39216;\cssrgb\c18431\c61176\c3922;\cssrgb\c65098\c49804\c34902;\cssrgb\c100000\c100000\c100000\c50196;\cssrgb\c78824\c17255\c17255;
}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \expnd0\expndtw0\kerning0
# this Code will help to schedule stop the RDS databasrs using Lambda\cf3 \
\cf2 # Yesh \cf3 \
\cf2 # Version -- 2.0\cf3 \
\
\pard\pardeftab720\partightenfactor0
\cf4 import\cf3  boto3\
\cf4 import\cf3  os\
\cf4 import\cf3  sys\
\cf4 import\cf3  time\
\cf4 from\cf3  datetime \cf4 import\cf3  datetime\cf5 ,\cf3  timezone\
\cf4 from\cf3  time \cf4 import\cf3  gmtime\cf5 ,\cf3  strftime\
\
\cf4 def\cf3  \cf6 shut_rds_all\cf5 ():\cf3 \
    region\cf7 \cb8 =\cf3 \cb1 os\cf5 .\cf3 environ\cf5 [\cf6 \'91us-east-1\'92\cf5 ]\cf3 \
    key\cf7 \cb8 =\cf3 \cb1 os\cf5 .\cf3 environ\cf5 [\cf6 \'91DEV-TEST\'92\cf5 ]\cf3 \
    value\cf7 \cb8 =\cf3 \cb1 os\cf5 .\cf3 environ\cf5 [\cf6 \'91Auto-Shutdown\'92\cf5 ]\cf3 \
\
    \
    client \cf7 \cb8 =\cf3 \cb1  boto3\cf5 .\cf3 client\cf5 (\cf6 'rds'\cf5 ,\cf3  region_name\cf7 \cb8 =\cf3 \cb1 region\cf5 )\cf3 \
    response \cf7 \cb8 =\cf3 \cb1  client\cf5 .\cf3 describe_db_instances\cf5 ()\cf3 \
    v_readReplica\cf7 \cb8 =\cf5 \cb1 []\cf3 \
    \cf4 for\cf3  i \cf4 in\cf3  response\cf5 [\cf6 'DBInstances'\cf5 ]:\cf3 \
        readReplica\cf7 \cb8 =\cf3 \cb1 i\cf5 [\cf6 'ReadReplicaDBInstanceIdentifiers'\cf5 ]\cf3 \
        v_readReplica\cf5 .\cf3 extend\cf5 (\cf3 readReplica\cf5 )\cf3 \
    \
    \cf4 for\cf3  i \cf4 in\cf3  response\cf5 [\cf6 'DBInstances'\cf5 ]:\cf3 \
\pard\pardeftab720\partightenfactor0
\cf2 #The if condition below filters aurora clusters from single instance databases as boto3 commands defer to stop the aurora clusters.\cf3 \
        \cf4 if\cf3  i\cf5 [\cf6 'Engine'\cf5 ]\cf3  \cf4 not\cf3  \cf4 in\cf3  \cf5 [\cf6 'aurora-mysql'\cf5 ,\cf6 'aurora-postgresql'\cf5 ]:\cf3 \
\cf2 #The if condition below filters Read replicas.\cf3 \
            \cf4 if\cf3  i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]\cf3  \cf4 not\cf3  \cf4 in\cf3  v_readReplica \cf4 and\cf3  \cf6 len\cf5 (\cf3 i\cf5 [\cf6 'ReadReplicaDBInstanceIdentifiers'\cf5 ])\cf3  \cf7 \cb8 ==\cf3 \cb1  \cf9 0\cf5 :\cf3 \
                arn\cf7 \cb8 =\cf3 \cb1 i\cf5 [\cf6 'DBInstanceArn'\cf5 ]\cf3 \
                resp2\cf7 \cb8 =\cf3 \cb1 client\cf5 .\cf3 list_tags_for_resource\cf5 (\cf3 ResourceName\cf7 \cb8 =\cf3 \cb1 arn\cf5 )\cf3 \
\cf2 #check if the RDS instance is part of the Auto-Shutdown group.\cf3 \
                \cf4 if\cf3  \cf9 0\cf7 \cb8 ==\cf6 \cb1 len\cf5 (\cf3 resp2\cf5 [\cf6 'TagList'\cf5 ]):\cf3 \
                    \cf4 print\cf5 (\cf6 'DB Instance \{0\} is not part of autoshutdown'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
                \cf4 else\cf5 :\cf3 \
                    \cf4 for\cf3  tag \cf4 in\cf3  resp2\cf5 [\cf6 'TagList'\cf5 ]:\cf3 \
\cf2 #If the tags match, then stop the instances by validating the current status.\cf3 \
                        \cf4 if\cf3  tag\cf5 [\cf6 'Key'\cf5 ]\cf7 \cb8 ==\cf3 \cb1 key \cf4 and\cf3  tag\cf5 [\cf6 'Value'\cf5 ]\cf7 \cb8 ==\cf3 \cb1 value\cf5 :\cf3 \
                            \cf4 if\cf3  i\cf5 [\cf6 'DBInstanceStatus'\cf5 ]\cf3  \cf7 \cb8 ==\cf3 \cb1  \cf6 'available'\cf5 :\cf3 \
                                client\cf5 .\cf3 stop_db_instance\cf5 (\cf3 DBInstanceIdentifier \cf7 \cb8 =\cf3 \cb1  i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ])\cf3 \
                                \cf4 print\cf5 (\cf6 'stopping DB instance \{0\}'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
                            \cf4 elif\cf3  i\cf5 [\cf6 'DBInstanceStatus'\cf5 ]\cf3  \cf7 \cb8 ==\cf3 \cb1  \cf6 'stopped'\cf5 :\cf3 \
                                \cf4 print\cf5 (\cf6 'DB Instance \{0\} is already stopped'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
                            \cf4 elif\cf3  i\cf5 [\cf6 'DBInstanceStatus'\cf5 ]\cf7 \cb8 ==\cf6 \cb1 'starting'\cf5 :\cf3 \
                                \cf4 print\cf5 (\cf6 'DB Instance \{0\} is in starting state. Please stop the cluster after starting is complete'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
                            \cf4 elif\cf3  i\cf5 [\cf6 'DBInstanceStatus'\cf5 ]\cf7 \cb8 ==\cf6 \cb1 'stopping'\cf5 :\cf3 \
                                \cf4 print\cf5 (\cf6 'DB Instance \{0\} is already in stopping state.'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
                        \cf4 elif\cf3  tag\cf5 [\cf6 'Key'\cf5 ]\cf7 \cb8 !=\cf3 \cb1 key \cf4 and\cf3  tag\cf5 [\cf6 'Value'\cf5 ]\cf7 \cb8 !=\cf3 \cb1 value\cf5 :\cf3 \
                            \cf4 print\cf5 (\cf6 'DB instance \{0\} is not part of autoshutdown'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
                        \cf4 elif\cf3  \cf6 len\cf5 (\cf3 tag\cf5 [\cf6 'Key'\cf5 ])\cf3  \cf7 \cb8 ==\cf3 \cb1  \cf9 0\cf3  \cf4 or\cf3  \cf6 len\cf5 (\cf3 tag\cf5 [\cf6 'Value'\cf5 ])\cf3  \cf7 \cb8 ==\cf3 \cb1  \cf9 0\cf5 :\cf3 \
                            \cf4 print\cf5 (\cf6 'DB Instance \{0\} is not part of auroShutdown'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
            \cf4 elif\cf3  i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]\cf3  \cf4 in\cf3  v_readReplica\cf5 :\cf3 \
                \cf4 print\cf5 (\cf6 'DB Instance \{0\} is a Read Replica. Cannot shutdown a Read Replica instance'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
            \cf4 else\cf5 :\cf3 \
                \cf4 print\cf5 (\cf6 'DB Instance \{0\} has a read replica. Cannot shutdown a database with Read Replica'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBInstanceIdentifier'\cf5 ]))\cf3 \
\
    response\cf7 \cb8 =\cf3 \cb1 client\cf5 .\cf3 describe_db_clusters\cf5 ()\cf3 \
    \cf4 for\cf3  i \cf4 in\cf3  response\cf5 [\cf6 'DBClusters'\cf5 ]:\cf3 \
        cluarn\cf7 \cb8 =\cf3 \cb1 i\cf5 [\cf6 'DBClusterArn'\cf5 ]\cf3 \
        resp2\cf7 \cb8 =\cf3 \cb1 client\cf5 .\cf3 list_tags_for_resource\cf5 (\cf3 ResourceName\cf7 \cb8 =\cf3 \cb1 cluarn\cf5 )\cf3 \
        \cf4 if\cf3  \cf9 0\cf7 \cb8 ==\cf6 \cb1 len\cf5 (\cf3 resp2\cf5 [\cf6 'TagList'\cf5 ]):\cf3 \
            \cf4 print\cf5 (\cf6 'DB Cluster \{0\} is not part of autoshutdown'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ]))\cf3 \
        \cf4 else\cf5 :\cf3 \
            \cf4 for\cf3  tag \cf4 in\cf3  resp2\cf5 [\cf6 'TagList'\cf5 ]:\cf3 \
                \cf4 if\cf3  tag\cf5 [\cf6 'Key'\cf5 ]\cf7 \cb8 ==\cf3 \cb1 key \cf4 and\cf3  tag\cf5 [\cf6 'Value'\cf5 ]\cf7 \cb8 ==\cf3 \cb1 value\cf5 :\cf3 \
                    \cf4 if\cf3  i\cf5 [\cf6 'Status'\cf5 ]\cf3  \cf7 \cb8 ==\cf3 \cb1  \cf6 'available'\cf5 :\cf3 \
                        client\cf5 .\cf3 stop_db_cluster\cf5 (\cf3 DBClusterIdentifier\cf7 \cb8 =\cf3 \cb1 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ])\cf3 \
                        \cf4 print\cf5 (\cf6 'stopping DB cluster \{0\}'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ]))\cf3 \
                    \cf4 elif\cf3  i\cf5 [\cf6 'Status'\cf5 ]\cf3  \cf7 \cb8 ==\cf3 \cb1  \cf6 'stopped'\cf5 :\cf3 \
                        \cf4 print\cf5 (\cf6 'DB Cluster \{0\} is already stopped'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ]))\cf3 \
                    \cf4 elif\cf3  i\cf5 [\cf6 'Status'\cf5 ]\cf7 \cb8 ==\cf6 \cb1 'starting'\cf5 :\cf3 \
                        \cf4 print\cf5 (\cf6 'DB Cluster \{0\} is in starting state. Please stop the cluster after starting is complete'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ]))\cf3 \
                    \cf4 elif\cf3  i\cf5 [\cf6 'Status'\cf5 ]\cf7 \cb8 ==\cf6 \cb1 'stopping'\cf5 :\cf3 \
                        \cf4 print\cf5 (\cf6 'DB Cluster \{0\} is already in stopping state.'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ]))\cf3 \
                \cf4 elif\cf3  tag\cf5 [\cf6 'Key'\cf5 ]\cf3  \cf7 \cb8 !=\cf3 \cb1  key \cf4 and\cf3  tag\cf5 [\cf6 'Value'\cf5 ]\cf3  \cf7 \cb8 !=\cf3 \cb1  value\cf5 :\cf3 \
                    \cf4 print\cf5 (\cf6 'DB Cluster \{0\} is not part of autoshutdown'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ]))\cf3 \
                \cf4 else\cf5 :\cf3 \
                    \cf4 print\cf5 (\cf6 'DB Instance \{0\} is not part of auroShutdown'\cf5 .\cf6 format\cf5 (\cf3 i\cf5 [\cf6 'DBClusterIdentifier'\cf5 ]))\cf3 \
\
\pard\pardeftab720\partightenfactor0
\cf4 def\cf3  \cf6 lambda_handler\cf5 (\cf3 event\cf5 ,\cf3  context\cf5 ):\cf3 \
    shut_rds_all\cf5 ()}