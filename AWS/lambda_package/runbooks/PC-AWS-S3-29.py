"""
Remediate Prisma Policy:

PC-AWS-S3-29: AWS S3 buckets are accessible to public

Description:

Removes S3 bucket public access at the bucket level.

Required Permissions:

- s3:PutBucketPublicAccessBlock

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Permissions",
      "Action": [
        "s3:PutBucketPublicAccessBlock"
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
  bucket_name  = alert['resource_id']
  region       = alert['region']
  account      = alert['account']['account_number']

  s3 = session.client('s3', region_name=region)

  try:
    bucket_acl = s3.get_bucket_acl(Bucket=bucket_name)
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  # Remove public access at bucket level
  try:
    response = s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        },
        ExpectedBucketOwner=account
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Public access removed from S3 bucket {}.'.format(bucket_name))

  return