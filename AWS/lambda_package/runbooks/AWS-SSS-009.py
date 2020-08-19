"""
Remediate Prisma Policy:

AWS:SSS-009 S3 Logging Enabled

Description:

S3 Logging provides a way for you to get details about S3 bucket activity. By default, AWS does not enable
logging for S3 buckets. This additional insight into bucket activity can be useful when troubleshooting and
may be requested by AWS Support. Logging cannot be enabled retroactive to an issue.

Required Permissions:

- sts:GetCallerIdentity
- s3:CreateBucket
- s3:GetBucketLogging
- s3:PutBucketLogging

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "STSPermissions",
      "Action": [
        "sts:GetCallerIdentity"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "S3Permissions",
      "Action": [
        "s3:CreateBucket",
        "s3:GetBucketLogging",
        "s3:PutBucketLogging"
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

  bucket_name = alert['resource_id']
  region = alert['region']

  s3  = session.client('s3', region_name=region)
  sts = session.client('sts', region_name=region)

  try:
    logging = s3.get_bucket_logging(Bucket=bucket_name)
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  # Is bucket logging already enabled?
  try:
    enabled = logging['LoggingEnabled']
  except KeyError:
    enabled = None

  if enabled != None:
    print('Logging already enabled for S3 bucket: {}.'.format(bucket_name))
    return

  # Grab the AWS account Id
  account_id = get_account_id(sts)

  # Create new target bucket OR return an existing one
  target_bucket = new_s3_bucket(s3, account_id, region) if (account_id != 'fail') else 'fail'

  # Enable bucket logging
  if target_bucket != 'fail':
    result = update_s3_bucket(s3, bucket_name, target_bucket)

  return


def get_account_id(sts):
  """
  Return AWS Account Id
  """

  try:
    account_id = sts.get_caller_identity()['Account']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  return account_id


def new_s3_bucket(s3, account_id, region):
  """
  Create new S3 target bucket OR return an existing one
  """

  target_bucket = 's3accesslogs-' + account_id + '-' + region

  try:
    if region == 'us-east-1':
      result = s3.create_bucket(
        ACL = 'log-delivery-write',
        Bucket = target_bucket
      )
    else:
      result = s3.create_bucket(
        ACL = 'log-delivery-write',
        Bucket = target_bucket,
        CreateBucketConfiguration = {'LocationConstraint': region}
      )

    print('New S3 target bucket created: {}'.format(target_bucket))

  except ClientError as e:
    if e.response['Error']['Code'] == 'BucketAlreadyExists':
      print('Using existing S3 target bucket: {}'.format(target_bucket))
    elif e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
      print('Using already owned and existing S3 target bucket: {}'.format(target_bucket))
    else:
      print(e.response['Error']['Message'])
      return 'fail'

  return target_bucket


def update_s3_bucket(s3, bucket_name, target_bucket):
  """
  Enable S3 bucket logging
  """

  try:
    result = s3.put_bucket_logging(
      Bucket = bucket_name,
      BucketLoggingStatus = {
        'LoggingEnabled': {
          'TargetBucket': target_bucket,
          'TargetPrefix': ''
        }
      }
    )
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    print('Logging enabled for S3 bucket: {}.'.format(bucket_name))

  return

