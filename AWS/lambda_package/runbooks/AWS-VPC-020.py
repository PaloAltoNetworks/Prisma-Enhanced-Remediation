"""
Remediate Prisma Policy:

AWS:VPC-020 VPC Flow Logs Not Enabled

Description:

VPC Flow Logs allows an organization to troubleshoot connectivity and security issues in a VPC.
Best security practice is to enable VPC Flow Logs on all VPCs.

Required Permissions:

- iam:PutRolePolicy
- iam:CreateRole
- iam:GetRole
- iam:PassRole
- logs:CreateLogGroup
- logs:PutRetentionPolicy
- ec2:CreateFlowLogs

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "IAMPermissions",
      "Action": [
        "iam:PutRolePolicy",
        "iam:CreateRole",
        "iam:GetRole",
        "iam:PassRole"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "CloudWatchLogsPermissions",
      "Action": [
        "logs:CreateLogGroup",
        "logs:PutRetentionPolicy"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "EC2Permissions",
      "Action": [
        "ec2:CreateFlowLogs"
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

# Options:
#
# AWS default IAM Role name for Flow Logs
#
default_role_name   = 'flowlogsRole'
default_policy_name = 'flowlogsPolicy'


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index_prisma.py
  """

  vpc_id = alert['resource_id']
  region = alert['region']

  iam  = session.client('iam', region_name=region)
  logs = session.client('logs', region_name=region)
  ec2  = session.client('ec2', region_name=region)

  # Create IAM Role and Policy
  role_arn = new_iam_role(iam)

  # Create CloudWatch Logs group
  log_group_name = new_log_group(logs, vpc_id) if (role_arn != 'fail') else 'fail'

  # Enable VPC Flow Logs
  flow_id = new_flow_logs(ec2, vpc_id, log_group_name, role_arn) if (log_group_name != 'fail') else 'fail'

  if flow_id != 'fail':
    print('VPC Flow Logs enabled for VPC: {}'.format(vpc_id))
  else:
    print('Failed to enable VPC Flow Logs for VPC: {}'.format(vpc_id))

  return


def new_iam_role(iam):
  """
  Create new IAM Role and Inline Policy
  """

  try:
    role = iam.create_role(
      Path = '/',
      RoleName = default_role_name,
      AssumeRolePolicyDocument = json.dumps(Templates.RolePolicy)
    )
    role_arn  = role['Role']['Arn']

    print('New IAM Role created: {}'.format(role_arn))

  except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
      role = iam.get_role(
        RoleName = default_role_name
      )
      role_arn  = role['Role']['Arn']

      print('Using existing IAM Role: {}'.format(role_arn))

    else:
      print(e.response['Error']['Message'])
      return 'fail'

  try:
    policy = iam.put_role_policy(
      RoleName = default_role_name,
      PolicyName = default_policy_name,
      PolicyDocument = json.dumps(Templates.LogsPolicy)
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  return role_arn


def new_log_group(logs, vpc_id):
  """
  Create CloudWatch Logs group
  """

  log_group_name = 'flowlogsGroup' + '-' + vpc_id

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

  return log_group_name
  

def new_flow_logs(ec2, vpc_id, log_group_name, role_arn):
  """
  Enable VPC Flow Logs
  """

  try:
    flow_logs = ec2.create_flow_logs(
      ResourceIds = [vpc_id],
      ResourceType = 'VPC',
      TrafficType = 'ALL',
      LogGroupName = log_group_name,
      DeliverLogsPermissionArn = role_arn
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  flow_id = flow_logs['FlowLogIds'][0]

  print('New Flow Logs created: {}'.format(flow_id))

  return flow_id


class Templates:

  RolePolicy =  {
                  'Version': '2012-10-17',
                  'Statement': [
                    {
                      'Sid': '',
                      'Effect': 'Allow',
                      'Principal': {
                        'Service': 'vpc-flow-logs.amazonaws.com'
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
                        'logs:CreateLogGroup',
                        'logs:CreateLogStream',
                        'logs:DescribeLogGroups',
                        'logs:DescribeLogStreams',
                        'logs:PutLogEvents'
                      ],
                      'Effect': 'Allow',
                      'Resource': '*'
                    }
                  ]
                }

