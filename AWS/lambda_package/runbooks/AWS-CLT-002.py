"""
Remediate Prisma Policy:

AWS:CLT-002 CloudTrail log not encrypted with SSE-KMS

Description:

CloudTrail configured to use SSE-KMS provides additional confidentiality controls on log data. To gain
access, users must have S3 read permission on the corresponding log bucket and must be granted decrypt
permission by the customer-created master keys (CMK) policy.

Required Permissions:

- cloudtrail:DescribeTrails
- cloudtrail:UpdateTrail
- s3:GetBucketLocation
- kms:CreateAlias
- kms:CreateKey

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudTrailPermissions",
      "Action": [
        "cloudtrail:DescribeTrails",
        "cloudtrail:UpdateTrail"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "S3Permissions",
      "Action": [
        "s3:GetBucketLocation"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "KMSPermissions",
      "Action": [
        "kms:CreateAlias",
        "kms:CreateKey"
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


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index.py
  """

  trail_name = alert['resource_id']
  region     = alert['region']

  clt = session.client('cloudtrail', region_name=region)
  s3  = session.client('s3', region_name=region)

  try:
    trail = clt.describe_trails(trailNameList=[ trail_name ], includeShadowTrails=False)['trailList']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  if not trail:
    print('Error: Unable to find Trail {}.'.format(trail_name))
    return

  # Check the Trail home region
  try:
    home_region = trail[0]['HomeRegion']
  except (KeyError, IndexError):
    print('Error: Unable to determine the home region for Trail {}.'.format(trail_name))
    return

  else:
    if home_region != region:
      return

  # Is the Trail KmsKeyId in-use?
  try:
    trail_key = trail[0]['KmsKeyId']
  except (KeyError, IndexError):
    trail_key = None

  if trail_key == None:

    # Grab the Trail Arn (we need the Account Id)
    try:
      trail_arn  = trail[0]['TrailARN']
    except (KeyError, IndexError):
      print('Error: Unable to find the ARN for Trail {}.'.format(trail_name))
      return

    else:
      account_id = trail_arn.split(':')[4]

    # Grab the Trail S3 logging bucket
    try:
      trail_bucket = trail[0]['S3BucketName']
    except (KeyError, IndexError):
      print('Error: Unable to find the S3 logging bucket for Trail {}.'.format(trail_name))
      return

    # Find the Trail S3 logging bucket location (region)
    # More info: https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
    try:
      bucket_region = s3.get_bucket_location(Bucket=trail_bucket)['LocationConstraint']
    except ClientError as e:
      print(e.response['Error']['Message'])
      return

    if not bucket_region: bucket_region = 'us-east-1'     # N. Virginia
    if bucket_region == 'EU': bucket_region = 'eu-west-1' # Ireland

    key_id = create_cmk(session, account_id, trail_name, bucket_region)

    if key_id != 'fail':
      update_trail_cmk(clt, trail_name, key_id)

  return


def update_trail_cmk(clt, trail_name, key_id):
  """
  Update Trail with CMK
  """

  try:
    clt.update_trail(
      Name = trail_name,
      KmsKeyId = key_id
    )
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    print('Updated Trail {} with KMS Customer Managed encryption Key: {}.'.format(trail_name, key_id))

  return


def create_cmk(session, account_id, trail_name, bucket_region):
  """
  Create Customer Managed Key (CMK)
  """

  # Create KMS client session in the same region as the Trail S3 logging bucket
  kms = session.client('kms', region_name=bucket_region)

  cmk_alias_name = 'alias/' + trail_name + '-cloudtrail-key'

  # Create CMK
  try:
    cmk = kms.create_key(
      Description = 'CMK for CloudTrail Logs',
      KeyUsage = 'ENCRYPT_DECRYPT',
      Origin = 'AWS_KMS',
      BypassPolicyLockoutSafetyCheck = True,
      Policy = json.dumps(KMSTemplate.CMKPolicy(account_id, bucket_region))
    ) 
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  else:
    key_id = cmk['KeyMetadata']['Arn']

  # Create CMK alias
  try:
    kms.create_alias(
      AliasName = cmk_alias_name,
      TargetKeyId = key_id
    )
  except ClientError as e:
    print(e.response['Error']['Message'])

  return key_id


class KMSTemplate:

  @staticmethod
  def CMKPolicy(account_id, bucket_region):

    Policy = {
               'Version': '2012-10-17',
               'Id': 'Key policy created by CloudTrail',
               'Statement': [
                 {
                   'Sid': 'Enable IAM User Permissions',
                   'Effect': 'Allow',
                   'Principal': {
                     'AWS': [
                       'arn:aws:iam::' + account_id + ':root'
                     ]
                   },
                   'Action': 'kms:*',
                   'Resource': '*'
                 },
                 {
                   'Sid': 'Allow CloudTrail to encrypt logs',
                   'Effect': 'Allow',
                   'Principal': {
                     'Service': 'cloudtrail.amazonaws.com'
                   },
                   'Action': 'kms:GenerateDataKey*',
                   'Resource': '*',
                   'Condition': {
                     'StringLike': {
                       'kms:EncryptionContext:aws:cloudtrail:arn': 'arn:aws:cloudtrail:*:' + account_id + ':trail/*'
                     }
                   }
                 },
                 {
                   'Sid': 'Allow CloudTrail to describe key',
                   'Effect': 'Allow',
                   'Principal': {
                     'Service': 'cloudtrail.amazonaws.com'
                   },
                   'Action': 'kms:DescribeKey',
                   'Resource': '*'
                 },
                 {
                   'Sid': 'Allow principals in the account to decrypt log files',
                   'Effect': 'Allow',
                   'Principal': {
                     'AWS': '*'
                   },
                   'Action': [
                     'kms:Decrypt',
                     'kms:ReEncryptFrom'
                   ],
                   'Resource': '*',
                   'Condition': {
                     'StringEquals': {
                       'kms:CallerAccount': account_id
                     },
                     'StringLike': {
                       'kms:EncryptionContext:aws:cloudtrail:arn': 'arn:aws:cloudtrail:*:' + account_id + ':trail/*'
                     }
                   }
                 },
                 {
                   'Sid': 'Allow alias creation during setup',
                   'Effect': 'Allow',
                   'Principal': {
                     'AWS': '*'
                   },
                   'Action': 'kms:CreateAlias',
                   'Resource': '*',
                   'Condition': {
                     'StringEquals': {
                       'kms:CallerAccount': account_id,
                       'kms:ViaService': 'ec2.' + bucket_region + '.amazonaws.com'
                     }
                   }
                 },
                 {
                   'Sid': 'Enable cross account log decryption',
                   'Effect': 'Allow',
                   'Principal': {
                     'AWS': '*'
                   },
                   'Action': [
                     'kms:Decrypt',
                     'kms:ReEncryptFrom'
                   ],
                   'Resource': '*',
                   'Condition': {
                     'StringEquals': {
                       'kms:CallerAccount': account_id
                     },
                     'StringLike': {
                       'kms:EncryptionContext:aws:cloudtrail:arn': 'arn:aws:cloudtrail:*:' + account_id + ':trail/*'
                     }
                   }
                 }
               ]
             }

    return Policy

