"""
Remediate Prisma Policy:

AWS:IAM-015 Unused IAM Access Keys

Description:

IAM users can access AWS resources using different types of credentials, such as passwords or access keys.
It is recommended that all credentials that have been unused in 90 or greater days be removed or deactivated.

Required Permissions:

- iam:GetAccessKeyLastUsed
- iam:UpdateAccessKey

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "IAMPermissions",
      "Action": [
        "iam:GetAccessKeyLastUsed",
        "iam:UpdateAccessKey"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
"""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from datetime import date


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index.py
  """

  key_id = alert['resource_id']
  region = alert['region']

  iam = session.client('iam', region_name=region)

  try:
    resp = iam.get_access_key_last_used(AccessKeyId=key_id)
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  user_name = resp['UserName']
  last_used = resp['AccessKeyLastUsed']['LastUsedDate'].date()

  today = date.today()
  delta = today - last_used

  if delta.days >= 90:
    result = deactivate_access_key(iam, key_id, user_name) 

  return


def deactivate_access_key(iam, key_id, user_name):
  """
  Deactivate IAM Access Key
  """

  try:
    result = iam.update_access_key(
      UserName = user_name,
      AccessKeyId = key_id,
      Status = 'Inactive'
    )
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    print('Deactivated access key {} for user {}.'.format(key_id, user_name))

  return

