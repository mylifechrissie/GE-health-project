# GE-health-project
Interview next round
####################################################
1.ec2lambda-tagging.py: 
  The above file contains a python script for tagging all EC2 instances with the required tags (environment:dev,contact:henatcheugoue@gmail.com,organization_id:1074)in the targeted region us-east-1. all EC2 instances must have the required tag, lambda in collaborations with SNS as a trigger when monitored by AWS eventbridge will trigger the lambda fucntion that will pass the required tag through a lambda function. 
  ######################################################
  2. rdsstartlambda.py: and rdsstoplambda.py, both scripts will stop and start rds instances at a scheduled interval by identifying the instances to stop or start through a specific tag. AWS eventbridge monitors the instances and stop/start instances within a scehdule period of time.
      
 
