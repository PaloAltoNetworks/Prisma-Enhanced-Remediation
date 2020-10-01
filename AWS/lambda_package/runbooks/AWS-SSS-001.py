"""
Remediate Prisma Policy:

AWS:SSS-001 S3 Object Versioning Not Enabled

Description:

S3 Object Versioning is an important capability in protecting your data within a bucket. Once you enable
Object Versioning, you cannot remove it; you can suspend Object Versioning at any time on a bucket if you
do not wish for it to persist.

Required Permissions:

- s3:PutBucketVersioning

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Permissions",
      "Action": [
        "s3:PutBucketVersioning"
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

  bucket = alert['resource_id']
  region = alert['region']

  s3 = session.client('s3', region_name=region)

  try:
    result = s3.put_bucket_versioning(
      Bucket = bucket,
      VersioningConfiguration = {
        'Status': 'Enabled'
      }
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  else:
    print('Object Versioning enabled for S3 bucket: {}.'.format(bucket))

  return

