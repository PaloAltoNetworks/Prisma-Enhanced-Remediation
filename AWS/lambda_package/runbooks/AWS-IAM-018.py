"""
Remediate Prisma Policy:

AWS:IAM-018 IAM Support Role Check

Description:

The best security practice is to assign the least privilege available for access control to a user's role
to manage incidents with AWS Support. "AWSSupportAccess" is the default policy for AWS.

Required Permissions:

- iam:AttachRolePolicy
- iam:CreateRole
- iam:CreateUser
- iam:GetPolicy

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "IAMPermissions",
      "Action": [
        "iam:AttachRolePolicy",
        "iam:CreateRole",
        "iam:CreateUser",
        "iam:GetPolicy"
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
# Default User, Role and Policy
#
support_role_name  = 'AWSSupportRole'
support_user_name  = 'AWSSupportUser'
support_policy_arn = 'arn:aws:iam::aws:policy/AWSSupportAccess'


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index_prisma.py
  """

  region = alert['region']

  iam = session.client('iam', region_name=region)

  try:
    policy = iam.get_policy(PolicyArn = support_policy_arn)['Policy']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  if policy['AttachmentCount'] <= 0:

    # Create IAM User
    user_arn = new_iam_user(iam)

    # Create IAM Role
    role_arn = new_iam_role(iam, user_arn) if (user_arn != 'fail') else 'fail'

    # Result
    if role_arn != 'fail':
      print('A Support Role has been created to manage incidents with AWS Support.')
    else:
      print('Failed to create a Support Role to manage incidents with AWS Support.')

  else:
    print('AWS Support policy has one or more attachments: {}'.format(support_policy_arn))

  return


def new_iam_user(iam):
  """
  Create new Support IAM User
  """

  try:
    user = iam.create_user(
      Path = '/',
      UserName = support_user_name
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  else:
    user_arn = user['User']['Arn']
    print('New IAM Support User created: {}'.format(user_arn))

    sleep(10)  # Wait for IAM resource to be available. >> Gotta be a better way.. { wait? get? }.

  return user_arn


def new_iam_role(iam, user_arn):
  """
  Create new Support IAM Role and attach AWS Managed Policy
  """

  try:
    role = iam.create_role(
      Path = '/',
      RoleName = support_role_name,
      AssumeRolePolicyDocument = json.dumps(Template.RolePolicy(user_arn))
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'

  else:
    role_arn  = role['Role']['Arn']
    print('New IAM Support Role created: {}'.format(role_arn))

  try:
    result = iam.attach_role_policy(
      RoleName = support_role_name,
      PolicyArn = support_policy_arn
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return 'fail'
    
  return role_arn


class Template():

  def RolePolicy(user_arn):

    Policy =  {
                'Version': '2008-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Principal': {
                      'AWS': user_arn
                    },
                    'Action': 'sts:AssumeRole'
                  }
                ]
              }

    return Policy

