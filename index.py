import boto3

# Initialize a session using Boto3
ec2 = boto3.client('ec2', region_name='your-region')
cloudwatch = boto3.client('cloudwatch', region_name='your-region')

import datetime

# Get metrics for a specific EC2 instance
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'your-instance-id'
        },
    ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=10),
    EndTime=datetime.datetime.utcnow(),
    Period=60,
    Statistics=['Average'],
)

print("CPU Utilization Metrics:", response)

# Create a CloudWatch alarm for high CPU utilization
alarm_response = cloudwatch.put_metric_alarm(
    AlarmName='HighCPUUtilization',
    AlarmDescription='Alarm when CPU exceeds 70%',
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:your-region:your-account-id:your-sns-topic'],
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'your-instance-id'
        },
    ],
    Period=300,
    EvaluationPeriods=1,
    Threshold=70.0,
    ComparisonOperator='GreaterThanThreshold',
)

print("Alarm created:", alarm_response)

import time

# Log CPU utilization every minute
while True:
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'your-instance-id'
            },
        ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=1),
        EndTime=datetime.datetime.utcnow(),
        Period=60,
        Statistics=['Average'],
    )

    cpu_utilization = response['Datapoints'][0]['Average'] if response['Datapoints'] else None
    print(f"CPU Utilization at {datetime.datetime.utcnow()}: {cpu_utilization}%")

    # Wait for one minute
    time.sleep(60)

# Delete the CloudWatch alarm
cloudwatch.delete_alarms(
    AlarmNames=['HighCPUUtilization']
)

print("Alarm deleted.")
