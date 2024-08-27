
# **Monitoring and Logging EC2 Metrics using CloudWatch**

## **Overview**

This project demonstrates how to monitor AWS EC2 instances using Amazon CloudWatch. You'll learn how to retrieve and analyze EC2 metrics, create CloudWatch alarms, and log important metrics over time. This is crucial for maintaining the health and performance of your AWS infrastructure.

## **Project Objectives**

- Set up Boto3 to interact with EC2 and CloudWatch.
- Retrieve real-time EC2 metrics, such as CPU utilization.
- Create a CloudWatch alarm that triggers when CPU utilization exceeds a specific threshold.
- Log EC2 metrics at regular intervals for monitoring purposes.

## **Prerequisites**

Before you begin, ensure you have the following:

- **AWS Account**: Access to an AWS account with necessary permissions for EC2 and CloudWatch.
- **Python Installed**: Python 3.x installed on your system.
- **Boto3 Installed**: Boto3 library installed (`pip install boto3`).
- **AWS CLI Configured**: AWS CLI configured with your credentials (`aws configure`).

## **Getting Started**

### **1. Set Up Boto3 and Initialize CloudWatch**

First, you'll need to initialize the Boto3 client for EC2 and CloudWatch:

```python
import boto3

# Initialize a session using Boto3
ec2 = boto3.client('ec2', region_name='your-region')
cloudwatch = boto3.client('cloudwatch', region_name='your-region')
```

### **2. Retrieve EC2 Metrics**

Next, retrieve metrics for your EC2 instances, such as CPU utilization:

```python
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
```

### **3. Create a CloudWatch Alarm**

Set up an alarm to monitor high CPU utilization and trigger notifications:

```python
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
```

### **4. Log EC2 Metrics**

Log the CPU utilization metrics every minute to monitor the instance performance:

```python
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
```

### **5. Cleanup**

Finally, delete the CloudWatch alarm when it's no longer needed:

```python
# Delete the CloudWatch alarm
cloudwatch.delete_alarms(
    AlarmNames=['HighCPUUtilization']
)

print("Alarm deleted.")
```

## **Real-Life Applications**

- **Critical Server Monitoring**: Ensure that your production servers are not overutilized.
- **Automated Alerts**: Trigger automatic alerts or scaling actions based on resource utilization.
- **Cost Optimization**: Monitor and optimize resource usage to reduce unnecessary costs.

## **Conclusion**

By completing this project, you've gained practical experience in monitoring and logging EC2 metrics using CloudWatch. This is a key skill for managing AWS infrastructure effectively.

---

This `README.md` provides a comprehensive overview and step-by-step instructions for the project. You can customize it further based on your specific implementation details.