import boto3 
import json
import logging 
from pprint import pprint  
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ec2 = boto3.client(service_name ='ec2', region_name="us-east-1")
Tags = [{'Key': 'Environment', 'Value': 'Dev'},
        {'Key': 'Capacity', 'Value': 'BAU'},
        {'Key': 'OrgID', 'Value': '01473'},
        {'Key': 'Contact', 'Value': 'henatcheugoue@gmail.com'}
        ]
org_id =  {'Key': 'OrgID', 'Value': '01473'}

def lambda_handler(event, context):
    try:
        for each_instance in event['Records']:
            con_todict = json.loads(each_instance['Sns']['Message'])
            instance_id = con_todict['detail']['instance-id']
    except Exception as e:
         logger.error(e)
    get_instanceId()    
       
       
def get_instanceId():
    for reservation in ec2.describe_instances()['Reservations']:
        for each_in in reservation['Instances']:
            instance_id = []
            if each_in.get('Tags') != Tags:
                instance_id.append(each_in['InstanceId'])
                ec2.create_tags(
                    Resources = instance_id,
                    Tags= Tags
                    )
            if org_id not in each_in.get('Tags'):
                ec2.create_tags(
                    Resources = instance_id,
                    Tags= org_id
                    )            
    return None    