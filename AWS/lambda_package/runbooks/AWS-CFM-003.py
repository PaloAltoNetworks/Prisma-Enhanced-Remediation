"""
Remediate Prisma Policy:

AWS:CFM-003 CFN Stack Termination Protection

Description:

You can prevent a stack from being accidentally deleted by enabling termination protection on the stack.
If a user attempts to delete a stack with termination protection enabled, the deletion fails and the stack
including its status remains unchanged.

Required Permissions:

- cloudformation:DescribeStacks
- cloudformation:UpdateTerminationProtection

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudFormationPermissions",
      "Action": [
        "cloudformation:DescribeStacks",
        "cloudformation:UpdateTerminationProtection"
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

  stack_id = alert['resource_id']
  region   = alert['region']

  cfn = session.client('cloudformation', region_name=region)

  try:
    stack = cfn.describe_stacks(StackName=stack_id)['Stacks']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  stack_name = stack[0]['StackName']

  # Don't check stack with a status of..
  if stack[0]['StackStatus'] in ("DELETE_COMPLETE", "DELETE_IN_PROGRESS", "DELETE_FAILED"):
    return

  if stack[0]['EnableTerminationProtection'] != True:
    result = enable_term_protection(cfn, stack_name)

  return


def enable_term_protection(cfn, stack_name):
  """
  Enable CloudFormation Termination Protection
  """

  try:
    result = cfn.update_termination_protection(StackName=stack_name, EnableTerminationProtection=True)
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Enabled termination protection for CloudFormation Stack {}.'.format(stack_name))

  return

