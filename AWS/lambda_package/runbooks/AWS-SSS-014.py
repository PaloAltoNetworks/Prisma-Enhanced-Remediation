"""
Remediate Prisma Policy:

AWS:SSS-014 S3 Server Side Encryption Not Enabled

Description:

S3 buckets now require Server Side Encryption on creation of all objects via bucket policy.

Required Permissions:

- s3:PutEncryptionConfiguration

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Permissions",
      "Action": [
        "s3:PutEncryptionConfiguration"
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
    result = s3.put_bucket_encryption(
      Bucket = bucket,
      ServerSideEncryptionConfiguration = {
        'Rules': [
          {
            'ApplyServerSideEncryptionByDefault': {
            'SSEAlgorithm': 'AES256'
            }
          },
        ]
      }
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  else:
    print('Server Side Encryption enabled for S3 bucket: {}.'.format(bucket))

  return

