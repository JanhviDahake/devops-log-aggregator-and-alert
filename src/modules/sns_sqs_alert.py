# Create an sqs queue using boto3
import boto3
import json
import time

# Initialize AWS clients
sqs = boto3.client('sqs')
sns = boto3.client('sns')

# === Step 1: Create SQS Queue ===
queue_name = 'my-test-queue'
sqs_response = sqs.create_queue(
    QueueName=queue_name,
    Attributes={
        'DelaySeconds': '0',
        'VisibilityTimeout': '60'
    }
)
queue_url = sqs_response['QueueUrl']
print("✅ Created SQS Queue:", queue_url)

# Get Queue ARN
queue_attrs = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['QueueArn']
)
queue_arn = queue_attrs['Attributes']['QueueArn']

# === Step 2: Create SNS Topic ===
topic_name = 'my-test-topic'
sns_response = sns.create_topic(Name=topic_name)
topic_arn = sns_response['TopicArn']
print("✅ Created SNS Topic:", topic_arn)

# === Step 3: Allow SNS to Publish to SQS ===
policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "Allow-SNS-SendMessage",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "SQS:SendMessage",
        "Resource": queue_arn,
        "Condition": {
            "ArnEquals": {
                "aws:SourceArn": topic_arn
            }
        }
    }]
}

sqs.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={
        'Policy': json.dumps(policy)
    }
)

# === Step 4: Subscribe SQS to SNS Topic ===
sns.subscribe(
    TopicArn=topic_arn,
    Protocol='sqs',
    Endpoint=queue_arn
)
print("✅ Subscribed SQS Queue to SNS Topic")

# === Step 5: Subscribe Email to SNS Topic ===
email_address = "your-email@example.com"  # <-- Replace with your email
sns.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint=email_address
)
print(f"📧 Confirmation email sent to {email_address}. Please confirm to start receiving alerts.")

# === Step 6: Publish a Message to SNS Topic ===
message_text = 'Hello from SNS! This will go to both email and SQS.'
sns.publish(
    TopicArn=topic_arn,
    Message=message_text,
    Subject='Test SNS Notification'
)
print("✅ Published message to SNS")

# === Step 7: Receive the Message from SQS ===
print("⏳ Waiting for message to arrive in SQS...")
time.sleep(5)

response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=5
)

messages = response.get('Messages', [])
if messages:
    for msg in messages:
        print("📨 Received message from SQS:", msg['Body'])
        # Delete the message after reading
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg['ReceiptHandle']
        )
        print("✅ Deleted message from SQS")
else:
    print("⚠️ No messages received from SQS")

# Jay
