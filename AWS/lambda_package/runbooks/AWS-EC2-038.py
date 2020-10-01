"""
Remediate Prisma Policy:

AWS:EC2-038 Default VPC Security Group Allows Traffic from All Protocols and Ports

Description:

The default security group within a VPC is not configured to restrict outbound traffic and limits
inbound traffic to resources within the same group.

While the default security group cannot be deleted, it can be configured in a way to mitigate risk
and increase security.

**Note: Remediation revokes all ingress and egress rules from the default security group in order to
        comply with CIS Benchmark 4.3.

Required Permissions:

- ec2:DescribeSecurityGroups
- ec2:RevokeSecurityGroupIngress
- ec2:RevokeSecurityGroupEgress

Sample IAM Policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2Permissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSecurityGroups",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupEgress"
            ],
            "Resource": [
                "*"
            ]
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

  sg_id  = alert['resource_id']
  region = alert['region']

  ec2 = session.client('ec2', region_name=region)

  try:
    group = ec2.describe_security_groups(GroupIds=[ sg_id, ])['SecurityGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  # Check for default security group
  if group[0]['GroupName'] != 'default':
    print('Security group {} is not the default.'.format(sg_id))
    return

  # Revoke all ingress permissions
  try:
    ingress_perms = group[0]['IpPermissions']
  except (IndexError, KeyError):
    ingress_perms = ''

  for ip_perm in ingress_perms:
    remove_sg_rule(ec2, sg_id, ip_perm, revoke='ingress')

  # Revoke all egress permissions
  try:
    egress_perms = group[0]['IpPermissionsEgress']
  except (IndexError, KeyError):
    egress_perms = ''

  for ip_perm in egress_perms:
    remove_sg_rule(ec2, sg_id, ip_perm, revoke='egress')

  return


def remove_sg_rule(ec2, sg_id, ip_perm, revoke):
  """
  Revoke Security Group Rules
  """

  revoke_args = {
    'GroupId' :  sg_id,
    'IpPermissions' : [ ip_perm ]
  }

  if revoke == 'ingress':
    try:
      ec2.revoke_security_group_ingress(**revoke_args)
    except ClientError as e:
      print(e.response['Error']['Message'])
      return

  elif revoke == 'egress':
    try:
      ec2.revoke_security_group_egress(**revoke_args)
    except ClientError as e:
      print(e.response['Error']['Message'])
      return
  else:
    return

  print('Revoked {} rule {} from default security group {}.'.format(revoke, ip_perm, sg_id))

  return

