How to run a script

python3 script.py '*' eu-central-1 <ACCESSKEY> <SECRETKEY>

This will output all instances (*) in eu-central-1 region

lambda can be triggered as well (tested on my own AWS acc(tf0.15.5))

aws lambda invoke --region eu-central-1 --function-name list-instances-ebsses --payload '{ "ec2filter": "*", "REGION": "eu-central-1" }' response.json

Unfortunatly I wasn't able to fully deploy lambda due to my accesskey/secretkey limitations (can't create a IAM role), and I cannot see what role lambda-ex does

(aws iam get-role --role-name lambda-ex

An error occurred (AccessDenied) when calling the GetRole operation: User: arn:aws:iam::115189082206:user/svc.115189082206.tda.cocustest is not authorized to perform: iam:GetRole on resource: role lambda-ex because no permissions boundary allows the iam:GetRole action)

Error: creating Lambda Function (list-instances-ebsses): operation error Lambda: CreateFunction, https response error StatusCode: 403, RequestID: 16918180-9ce8-4699-a445-dcfbbd40f555, api error AccessDeniedException: User: arn:aws:iam::115189082206:user/svc.115189082206.tda.cocustest is not authorized to perform: iam:PassRole on resource: arn:aws:iam::115189082206:role/lambda-ex because no permissions boundary allows the iam:PassRole action

This was tested on both 0.15.5 and 0.12.31
