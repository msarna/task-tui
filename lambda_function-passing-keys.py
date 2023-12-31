import boto3

def lambda_handler(event, context):
    ec2filter = event['ec2filter']
    REGION = event['REGION']
    ACCESS_KEY = event['ACCESS_KEY']
    SECRET = event['SECRET']

    instances_info = []
    instance_sums = 0

    ec2client = boto3.client('ec2', region_name=REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET)
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

    sorted_instances_info = sorted(instances_info, key=lambda x: x[5], reverse=True)

    volume = ec2client.describe_volumes()
    for _volume in volume['Volumes']:
        size_gb = _volume['Size']
        instance_sums = instance_sums + size_gb

    return {
        'sorted_instances_info': sorted_instances_info,
        'all_ebs_storage': instance_sums
    }