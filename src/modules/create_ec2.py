# Create an ec2 instance using boto3 to replicate a producer, 
# it should expose an endpoint which when executed should log an event to the sqs queue
import boto3

# Initialize EC2 client
ec2 = boto3.client('ec2')

# Launch instance
response = ec2.run_instances(
    ImageId='ami-0418306302097dbff',  # Amazon Linux 2 (us-west-2)
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='string',  # Replace with your existing key pair name
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'LogGeneratorInstance'}
            ]
        }
    ],
    SecurityGroupIds=['your-security-group-id'],  # Replace with your security group ID
)

print("EC2 instance launched successfully!")
print("Instance ID:", response['Instances'][0]['InstanceId'])

# Jahnvi
