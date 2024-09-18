import boto3
import sys

def create_sns_topic(topic_name):
    """Create an SNS topic if it doesn't already exist."""
    # Create a client with AWS SNS
    sns_client = boto3.client('sns')
    
    # Attempt to create the topic
    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']
        print(f"Created new SNS topic: {topic_arn}")
        return topic_arn
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_topic.py <topic_name>")
        sys.exit(1)

    topic_name = sys.argv[1]
    create_sns_topic(topic_name)
