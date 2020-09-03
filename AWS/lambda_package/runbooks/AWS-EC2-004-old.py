"""
Remediate Prisma Policy:

AWS:EC2-004 Global Admin Port Access - RDP (TCP Port 3389) Detected

Description:

Global permission to access the well-known services TCP port 3389 (RDP) should not be allowed in a
security group.

**Note: Remediation will be executed if the well-known service is found within a port range.

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

import json
import re
import boto3
from botocore.exceptions import ClientError

# Options:
#
# Example
#   admin_port_list = [ 'tcp-22', 'tcp-23', 'tcp-3389' ]
#
admin_port_list  = [ 'tcp-3389' ]
global_cidr_list = [ '0.0.0.0/0', '::/0' ]


def remediate(session, alert, lambda_context):
  """
  Main Function invoked by index.py
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
    try:
      from_port   = ip_perm['FromPort']
    except KeyError:
      continue
    else:
      to_port     = ip_perm['ToPort']
      ip_protocol = ip_perm['IpProtocol']

    # Look for IPv4 permissions
    if ip_perm['IpRanges']:
      IpRanges = 'IpRanges'
      IpCidr   = 'CidrIp'

      for ip_range in ip_perm['IpRanges']:
        cidr_ip = ip_range['CidrIp']
        remove_sg_rule(ec2, sg_id, from_port, to_port, ip_protocol, cidr_ip, IpRanges, IpCidr)

    # Look for IPv6 permissions
    if ip_perm['Ipv6Ranges']:
      IpRanges = 'Ipv6Ranges'
      IpCidr   = 'CidrIpv6'

      for ip_range in ip_perm['Ipv6Ranges']:
        cidr_ip = ip_range['CidrIpv6']
        remove_sg_rule(ec2, sg_id, from_port, to_port, ip_protocol, cidr_ip, IpRanges, IpCidr)

  return


def remove_sg_rule(ec2, sg_id, from_port, to_port, ip_protocol, cidr_ip, IpRanges, IpCidr):
  """
  Revoke Ingress Security Group Rule
  """

  for admin_port in admin_port_list:
    proto = re.split('-', admin_port)[0]
    port  = re.split('-', admin_port)[1]

    find_port='true' if from_port <= int(port) <= to_port else 'false'

    if cidr_ip in global_cidr_list and ip_protocol.lower() == proto and find_port == 'true':

      revoke_args = {
        'GroupId' :  sg_id,
        'IpPermissions' : [
          {
            'IpProtocol': ip_protocol,
            'FromPort': from_port,
            'ToPort': to_port,
             IpRanges: [{ IpCidr: cidr_ip }]
          }
        ]
      }

      try:
        ec2.revoke_security_group_ingress(**revoke_args)

        print('Revoked rule permitting {}/{:d}-{:d} with cidr {} from {}.'.format(ip_protocol, from_port, to_port, cidr_ip, sg_id))

      except ClientError as e:
        print(e.response['Error']['Message'])

  return
