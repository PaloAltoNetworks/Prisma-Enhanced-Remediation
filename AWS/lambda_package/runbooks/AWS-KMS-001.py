"""
Remediate Prisma Policy:

AWS:KMS-001 KMS Key Rotation Disabled

Description:

The recommended best security practice is to allow for the KMS rotation of a Customer Master Key (CMK).

Enabling the rotation of CMKs will create a new version of the backing key for each rotation.

Required Permissions:

- kms:EnableKeyRotation

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "KMSPermissions",
      "Action": [
        "kms:EnableKeyRotation"
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

  key_id = alert['resource_id']
  region = alert['region']

  kms = session.client('kms', region_name=region)

  try:
    result = kms.enable_key_rotation(KeyId = key_id)
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  else:
    print('KMS key rotation enabled for Customer Master Key: {}.'.format(key_id))

  return

