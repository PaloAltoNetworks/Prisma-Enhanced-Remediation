"""
Remediate Prisma Policy:

AWS:EC2-031 Unused Security Groups

Description:

Unused security groups pose a risk against your AWS Infrastructure, as they are often unmaintained,
legacy, or improperly created. Failing to remove these unused security groups could lead to inadvertent
use of them, creating open attack surfaces in your infrastructure.

Required Permissions:

- ec2:DeleteSecurityGroup
- ec2:DescribeSecurityGroups
- lambda:ListFunctions

Sample IAM Policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2LambdaPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteSecurityGroup",
                "ec2:DescribeSecurityGroups",
                "lambda:ListFunctions"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
"""

import boto3
from botocore.exceptions import ClientError


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index_prisma.py
  """

  sg_id  = alert['resource_id']
  region = alert['region']

  ec2 = session.client('ec2', region_name=region)
  lam = session.client('lambda', region_name=region)

  # Check to see if the security group is tied to a Lambda function
  try:
    functions = lam.list_functions()['Functions']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  check = False

  for function in functions:
    if check == True:
      print('Security group {} is tied to a Lambda function. No remediation performed.'.format(sg_id))
      return

    try:
      vpc_config = function['VpcConfig']
    except KeyError:
      continue
    else:
      security_groups = vpc_config['SecurityGroupIds']

      for group in security_groups:
        if group == sg_id:
          check = True

  # Remediate (security group is not tied to a Lambda function)
  result = delete_unused_sg(ec2, sg_id)

  return


def delete_unused_sg(ec2, sg_id):
  """
  Delete Unused Security Group
  """

  try:
    result = ec2.delete_security_group(GroupId=sg_id)
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Removed unused security group {}.'.format(sg_id))

  return

