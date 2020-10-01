"""
Remediate Prisma Policy:

AWS:CLT-004 CloudTrail logs not integrated with CloudWatch

Description:

CloudTrail logs are not automatically sent to CloudWatch Logs. CloudWatch integration facilitates real-time
and historic activity logging based on user, API, resource, and IP address. It will also establish alarms and
notifications for anomalous or sensitive account activity.

Required Permissions:

- iam:CreateRole
- iam:GetRole
- iam:PutRolePolicy
- logs:CreateLogGroup
- logs:DescribeLogGroups
- logs:PutRetentionPolicy
- cloudtrail:UpdateTrail

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "IAMPermissions",
      "Action": [
        "iam:CreateRole",
        "iam:GetRole",
        "iam:PutRolePolicy"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "CloudWatchLogsPermissions",
      "Action": [
        "logs:CreateLogGroup",
        "logs:DescribeLogGroups",
        "logs:PutRetentionPolicy"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "CloudTrailPermissions",
      "Action": [
        "cloudtrail:UpdateTrail"
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

# Options:
#
# AWS IAM Role/ Policy and CloudWatch Logs Group Name
#
role_name   = 'CloudTrail_CloudWatchLogs_Role'
policy_name = 'CWLogsAllowDeliveryPolicy'
log_group_name = 'CloudTrail/DefaultLogGroup'


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index_prisma.py
  """

  trail_name = alert['resource_id']
  region     = alert['region']

  iam  = session.client('iam', region_name=region)
  logs = session.client('logs', region_name=region)
  clt  = session.client('cloudtrail', region_name=region)

  # Create IAM Role and Policy
  role_arn = new_iam_role(iam)

  # Create CloudWatch Logs group
  log_group_arn = new_log_group(logs) if (role_arn != 'fail') else 'fail'

  # Update Trail
  trail_status = update_trail(clt, trail_name, log_group_arn, role_arn) if (log_group_arn != 'fail') else 'fail'

  # Result
  if trail_status != 'fail':
    print('Integrated Trail {} with CloudWatch Logs group {}.'.format(trail_name, log_group_name))
  else:
    print('Failed to integrated Trail {} with CloudWatch Logs.'.format(trail_name))

  return


def new_iam_role(iam):
  """
  Create new IAM Role and Inline Policy
  """

  try:
    role = iam.create_role(
      Path = '/',
      RoleName = role_name,
      AssumeRolePolicyDocument = json.dumps(Templates.RolePolicy)
    )
    role_arn  = role['Role']['Arn']

    print('New IAM Role created: {}'.format(role_arn))

  except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
      role = iam.get_role(
        RoleName = role_name
      )
      role_arn  = role['Role']['Arn']

      print('Using existing IAM Role: {}'.format(role_arn))

    else:
      print(e.response['Error']['Message'])
      return 'fail'

  try:
    policy = iam.put_role_policy(
      RoleName = role_name,
      PolicyName = policy_name,
      PolicyDocument = json.dumps(Templates.LogsPolicy)
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  sleep(10)  # Wait for IAM resource to be available. >> Gotta be a better way.. { wait? get? }.

  return role_arn


def new_log_group(logs):
  """
  Create CloudWatch Logs group
  """

  try:
    group = logs.create_log_group(
      logGroupName = log_group_name
    )

    print('New CloudWatch Logs group created: {}'.format(log_group_name))

  except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
      print('Using existing CloudWatch Log group: {}'.format(log_group_name))
    else:
      print(e.response['Error']['Message'])
      return 'fail'

  try:
    retention = logs.put_retention_policy(
      logGroupName = log_group_name,
      retentionInDays = 30
    )
  except ClientError as e:
    print(e.response['Error']['Message'])

  try:
    log_group = logs.describe_log_groups(logGroupNamePrefix = log_group_name)['logGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  else:
    log_group_arn = log_group[0]['arn']

  return log_group_arn
  

def update_trail(clt, trail_name, log_group_arn, role_arn):
  """
  Update Trail to integrate with CloudWatch Logs
  """

  try:
    result = clt.update_trail(
      Name = trail_name,
      CloudWatchLogsLogGroupArn = log_group_arn,
      CloudWatchLogsRoleArn = role_arn,
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  return


class Templates:

  RolePolicy =  {
                  'Version': '2012-10-17',
                  'Statement': [
                    {
                      'Sid': '',
                      'Effect': 'Allow',
                      'Principal': {
                        'Service': 'cloudtrail.amazonaws.com'
                      },
                      'Action': 'sts:AssumeRole'
                    }
                  ]
                }

  LogsPolicy =  {
                  'Version': '2012-10-17',
                  'Statement': [
                    {
                      'Action': [
                        'logs:CreateLogStream',
                        'logs:PutLogEvents'
                      ],
                      'Effect': 'Allow',
                      'Resource': '*'
                    }
                  ]
                }

