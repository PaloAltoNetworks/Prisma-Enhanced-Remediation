"""
Remediate Prisma Policy:

AWS:EC2-039 Global Access on All Ports Detected

Description:

Global permission to access all ports should not be allowed in a security group. Best security practice
dictates restricting access to service ports solely to known static IP addresses within your control.

Required Permissions:

- ec2:DescribeSecurityGroups
- ec2:RevokeSecurityGroupIngress

Sample IAM Policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2Permissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSecurityGroups",
                "ec2:RevokeSecurityGroupIngress"
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

# Options:
#
global_cidr_list = [ '0.0.0.0/0', '::/0' ]


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index_prisma.py
  """

  sg_id  = alert['resource_id']
  region = alert['region']

  ec2   = session.client('ec2', region_name=region)

  try:
    group = ec2.describe_security_groups(GroupIds=[ sg_id, ])['SecurityGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  try:
    ip_perms = group[0]['IpPermissions']
  except (IndexError, KeyError):
    print('IP permissions not found for security group {}.'.format(sg_id))
    return

  for ip_perm in ip_perms:
    result = remove_offending_sg_rules(ec2, sg_id, ip_perm)

  return


def remove_sg_rule(ec2, revoke_args):
  """
  Revoke ingress security group rule
  """

  try:
    ec2.revoke_security_group_ingress(**revoke_args)
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  else:
    print('Revoked security group rule: {}.'.format(revoke_args))

  return


def remove_offending_sg_rules(ec2, sg_id, ip_perm):
  """
  Remove offending security group rules (calls >> remove_sg_rule())
  """

  # Look for IPv4 permissions
  if ip_perm['IpRanges']:

    for ip_range in ip_perm['IpRanges']:
      if ip_range['CidrIp'] in global_cidr_list:

        if (ip_perm['IpProtocol'] == '-1'):
          revoke_args = {
            'GroupId' : sg_id,
            'IpPermissions' : [
              {
                'IpProtocol': ip_perm['IpProtocol'],
                'IpRanges': [{ 'CidrIp': ip_range['CidrIp'] }]
              }
            ]
          }

        elif (ip_perm['FromPort'] == 0 and ip_perm['ToPort'] == 65535):
          revoke_args = {
            'GroupId' : sg_id,
            'IpPermissions' : [
              {
                'IpProtocol': ip_perm['IpProtocol'],
                'FromPort': ip_perm['FromPort'],
                'ToPort': ip_perm['ToPort'],
                'IpRanges': [{ 'CidrIp': ip_range['CidrIp'] }]
              }
            ]
          }
        else:
          revoke_args = None

        if revoke_args != None:
          result = remove_sg_rule(ec2, revoke_args)

  # Look for IPv6 permissions
  if ip_perm['Ipv6Ranges']:

    for ip_range in ip_perm['Ipv6Ranges']:
      if ip_range['CidrIpv6'] in global_cidr_list:

        if (ip_perm['IpProtocol'] == '-1'):
          revoke_args = {
            'GroupId' :  sg_id,
            'IpPermissions' : [
              {
                'IpProtocol': ip_perm['IpProtocol'],
                'Ipv6Ranges': [{ 'CidrIpv6': ip_range['CidrIpv6'] }]
              }
            ]
          }

        elif (ip_perm['FromPort'] == 0 and ip_perm['ToPort'] == 65535):
          revoke_args = {
            'GroupId' :  sg_id,
            'IpPermissions' : [
              {
                'IpProtocol': ip_perm['IpProtocol'],
                'FromPort': ip_perm['FromPort'],
                'ToPort': ip_perm['ToPort'],
                'Ipv6Ranges': [{ 'CidrIpv6': ip_range['CidrIpv6'] }]
              }
            ]
          }
        else:
          revoke_args = None

        if revoke_args != None:
          result = remove_sg_rule(ec2, revoke_args)

  return

