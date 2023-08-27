import boto3
import sys
from tabulate import tabulate

if len(sys.argv) != 5:
    print("Please pass all required arguments")
    exit(1)

ec2filter = sys.argv[1]
REGION = sys.argv[2]
ACCESS_KEY = sys.argv[3]
SECRET = sys.argv[4]

instances_info = []
instance_sums = 0
instance_sums_filtered = 0

ec2client = boto3.client('ec2',region_name=REGION,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET)
response = ec2client.describe_instances(Filters=[{"Name" :"tag:Name", "Values":[ec2filter]}])

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_name = instance['Tags'][0]['Value']
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        public_ip = instance.get('PublicIpAddress', 'N/A')
        volume = ec2client.describe_volumes(Filters=[{'Name':'attachment.instance-id','Values':[instance_id]}])
        size_gb = 0
        for _volume in volume['Volumes']:
            size_gb = _volume['Size'] + size_gb


        instance_details = (instance_name, instance_id, instance_type, state, private_ip, public_ip, size_gb)
        instances_info.append(instance_details)

for item in instances_info:
    instance_sums_filtered = item[6] + instance_sums_filtered

sorted_instances_info = sorted(instances_info, key=lambda x: x[6], reverse=True)

table_headers = ['Instance Name','Instance ID', 'Instance Type', 'State', 'Private IP', 'Public IP', 'EBS Size (GB)']
table_data = [(item[0], item[1], item[2], item[3], item[4], item[5], item[6]) for item in sorted_instances_info]
formatted_table = tabulate(table_data, headers=table_headers, tablefmt='grid')

print(formatted_table)

print(f"All EBS storage OF FILTERED SERVERS :{instance_sums_filtered}")

volume = ec2client.describe_volumes()
for _volume in volume['Volumes']:
    size_gb = _volume['Size']
    instance_sums = instance_sums + size_gb

print(f"\nAll EBS storage: {instance_sums}")