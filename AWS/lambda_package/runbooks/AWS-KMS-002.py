"""
Remediate Prisma Policy:

AWS:KMS-002: KMS Key Scheduled for Deletion

Description:

The recommended action to remedy this problem is to cancel this deletion and disable the key instead.

The minimum amount of time required for scheduling a key deletion is seven days allowing for a pending deletion operation to be canceled before the deletion date.

Required Permissions:

- kms:DescribeKey
- kms:DisableKey
- kms:CancelKeyDeletion

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "KMSPermissions",
      "Action": [
	      "kms:DescribeKey",
        "kms:DisableKey",
        "kms:CancelKeyDeletion"
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
  Main Function invoked by index_prisma.py
  """

  key_id = alert['resource_id']
  region = alert['region']

  kms = session.client('kms', region_name=region)

  try:
    key_metadata = kms.describe_key(KeyId = key_id)['KeyMetadata']
  
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  key_status = key_metadata['KeyState']
  
  if key_status == "PendingDeletion":
    try:
      result = kms.cancel_key_deletion(KeyId = key_id)
 
    except ClientError as e:
      print(e.response['Error']['Message'])
      return

    try:
      result = kms.disable_key(KeyId = key_id)
    except ClientError as e:
      print(e.response['Error']['Message'])
    else:
      print('KMS key disabled for Customer Master Key: {}.'.format(key_id))
  return
