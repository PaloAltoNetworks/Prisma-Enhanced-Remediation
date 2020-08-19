"""
Remediate Prisma Policy:

AWS:VPC-013 VPC Elastic IP Limit

Description:

If your account is approaching the Elastic IP limitation per region, this remediation script will attempt
to release any/all unassociated EIPs.

Required Permissions:

- ec2:DescribeAddresses
- ec2:ReleaseAddress

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EC2Permissions",
      "Action": [
        "ec2:DescribeAddresses",
        "ec2:ReleaseAddress"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
"""

import boto3
from botocore.exceptions import ClientError


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index.py
  """

  resource = None
  region   = alert['region']

  ec2 = session.client('ec2', region_name=region)

  try:
    eips = ec2.describe_addresses()['Addresses']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  unassociated = []

  for eip in eips:
    if 'AssociationId' not in eip:
      unassociated.append(eip['AllocationId'])

  for id in unassociated:
    try:
      result = ec2.release_address(AllocationId=id)
    except ClientError as e:
      print(e.response['Error']['Message'])
    else:
      print('Released unassociated EIP {} in the {} region.'.format(id, region))

  return

