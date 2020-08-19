"""
Remediate Prisma Policy:

AWS:CONFIG-001 AWS Config is not enabled

Description:

The AWS Config service provides visibility to user configuration history and configuration change
notifications. Along with use of CloudTrail, we consider enabling AWS Config to be a best practice for users.

**Note: No Config Rules are created.

Required Permissions:

- iam:AttachRolePolicy
- iam:CreateRole
- iam:GetRole
- s3:CreateBucket
- s3:PutBucketPolicy
- config:PutConfigurationRecorder
- config:PutDeliveryChannel
- config:StartConfigurationRecorder

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "IAMPermissions",
      "Action": [
        "iam:AttachRolePolicy",
        "iam:CreateRole",
        "iam:GetRole"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "S3Permissions",
      "Action": [
        "s3:CreateBucket",
        "s3:PutBucketPolicy"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "ConfigPermissions",
      "Action": [
        "config:PutConfigurationRecorder",
        "config:PutDeliveryChannel",
        "config:StartConfigurationRecorder"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
"""

import json
import boto3
from botocore.exceptions import ClientError
from time import sleep


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index.py
  """

  region = alert['region']

  iam  = session.client('iam', region_name=region)
  s3   = session.client('s3', region_name=region)
  config = session.client('config', region_name=region)

  # Create IAM Role
  role_arn, account_id = new_iam_role(iam, region)

  # Create Config Recorder
  recorder_name = new_config_recorder(config, role_arn) if (role_arn != 'fail') else 'fail'

  # Create S3 Bucket
  bucket_name   = new_s3_bucket(s3, account_id, region) if (role_arn != 'fail') else 'fail'

  # Create Config Delivery Channel
  channel_name  = new_config_channel(config, bucket_name) if (bucket_name != 'fail') else 'fail'

  # Start Config Recorder
  start_result  = start_recorder(config, recorder_name) if (channel_name != 'fail' and recorder_name != 'fail') else 'fail'

  # Results
  if start_result != 'fail':
    print('AWS Config enabled in region {}.'.format(region))
  else:
    print('Failed to enable AWS Config in region {}.'.format(region))

  return


def new_iam_role(iam, region):
  """
  Create new IAM Role and attach AWS Config Managed Policy
  """

  role_name = 'config-role-' + region

  try:
    role = iam.create_role(
      Path = '/',
      RoleName = role_name,
      AssumeRolePolicyDocument = json.dumps(RoleTemplate.RolePolicy)
    )
    role_arn = role['Role']['Arn']

    print('New IAM Role created: {}'.format(role_arn))
    sleep(10)  # Wait for IAM resource to be available. >> Gotta be a better way.. { wait? get? }.

  except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
      role = iam.get_role(
        RoleName = role_name
      )
      role_arn = role['Role']['Arn']

      print('Using existing IAM Role: {}'.format(role_arn))

    else:
      print(e.response['Error']['Message'])
      return 'fail', None

  try:
    result = iam.attach_role_policy(
      RoleName = role_name,
      PolicyArn = 'arn:aws:iam::aws:policy/service-role/AWSConfigRole'
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail', None

  account_id = role_arn.split(':')[4]

  return role_arn, account_id


def new_s3_bucket(s3, account_id, region):
  """
  Create new S3 Bucket
  """

  bucket_name = 'config-bucket-' + account_id

  try:
    if region == 'us-east-1':
      result = s3.create_bucket(
        ACL = 'private',
        Bucket = bucket_name
      )
    else:
      result = s3.create_bucket(
        ACL = 'private',
        Bucket = bucket_name,
        CreateBucketConfiguration = {'LocationConstraint': region}
      )

    print('New S3 bucket created: {}'.format(bucket_name))

  except ClientError as e:
    if e.response['Error']['Code'] == 'BucketAlreadyExists':
      print('Using existing S3 bucket: {}'.format(bucket_name))
    elif e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
      print('Using already owned and existing S3 bucket: {}'.format(bucket_name))
    else:
      print(e.response['Error']['Message'])
      return 'fail'

  try:
    result = s3.put_bucket_policy(
      Bucket = bucket_name,
      Policy = json.dumps(BucketTemplate.BucketPolicy(bucket_name, account_id))
    )
  except ClientError as e:
      print(e.response['Error']['Message'])
      return 'fail'

  return bucket_name
  

def new_config_recorder(config, role_arn):
  """
  Create new Config Recorder
  """

  recorder_name = 'default'

  try:
    result = config.put_configuration_recorder(
      ConfigurationRecorder = {
        'name': recorder_name,
        'roleARN': role_arn,
        'recordingGroup': {
            'allSupported': True
        }
      }
    )

    print('New Config recorder created: {}'.format(recorder_name))

  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  return recorder_name


def new_config_channel(config, bucket_name):
  """
  Create new Config Delivery Channel
  """

  channel_name = 'default'

  try:
    result = config.put_delivery_channel(
      DeliveryChannel = {
        'name': channel_name,
        's3BucketName': bucket_name,
        'configSnapshotDeliveryProperties': {
          'deliveryFrequency': 'One_Hour'
        }
      }
    )

    print('New Config delivery channel created: {}'.format(channel_name))

  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  return channel_name


def start_recorder(config, recorder_name):
  """
  Start Config Recorder
  """

  try:
    result = config.start_configuration_recorder(
      ConfigurationRecorderName = recorder_name
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  return


class RoleTemplate:

  RolePolicy = {
                 'Version': '2012-10-17',
                 'Statement': [
                   {
                     'Sid': '',
                     'Effect': 'Allow',
                     'Principal': {
                       'Service': 'config.amazonaws.com'
                     },
                     'Action': 'sts:AssumeRole'
                   }
                 ]
               }

class BucketTemplate():

  def BucketPolicy(bucket_name, account_id):

    Policy = {
               'Version': '2012-10-17',
               'Statement': [
                 {
                   'Sid': 'AWSConfigBucketPermissionsCheck',
                   'Effect': 'Allow',
                   'Principal': {
                     'Service': [
                       'config.amazonaws.com'
                     ]
                   },
                   'Action': 's3:GetBucketAcl',
                   'Resource': 'arn:aws:s3:::' + bucket_name
                 },
                 {
                   'Sid': ' AWSConfigBucketDelivery',
                   'Effect': 'Allow',
                   'Principal': {
                     'Service': [
                       'config.amazonaws.com'    
                     ]
                   },
                   'Action': 's3:PutObject',
                   'Resource': 'arn:aws:s3:::' + bucket_name + '/AWSLogs/' + account_id + '/Config/*',
                   'Condition': { 
                     'StringEquals': { 
                       's3:x-amz-acl': 'bucket-owner-full-control' 
                     }
                   }
                 }
               ]
             }   

    return Policy

