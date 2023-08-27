import boto3
import sys

ec2filter = sys.argv[1]
REGION = sys.argv[2]
ACCESS_KEY = sys.argv[3]
SECRET = sys.argv[4]

instances_info = []
instance_sums = 0

ec2client = boto3.client('ec2',region_name=REGION,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET)
response = ec2client.describe_instances(Filters=[{"Name" :"tag:Name", "Values":[ec2filter]}])

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        public_ip = instance.get('PublicIpAddress', 'N/A')
        volume = ec2client.describe_volumes(Filters=[{'Name':'attachment.instance-id','Values':[instance_id]}])
        size_gb = 0
        for _volume in volume['Volumes']:
            size_gb = _volume['Size'] + size_gb


        instance_details = (instance_id, instance_type, state, private_ip, public_ip, size_gb)
        instances_info.append(instance_details)

print(sorted(instances_info, key=lambda size_gb: size_gb[5], reverse=True))


volume = ec2client.describe_volumes()
for _volume in volume['Volumes']:
    size_gb = _volume['Size']
    instance_sums = instance_sums + size_gb

print(f"\nAll EBS storage: {instance_sums}")