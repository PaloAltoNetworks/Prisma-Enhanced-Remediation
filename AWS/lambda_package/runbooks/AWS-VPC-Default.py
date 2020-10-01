"""
Remediate Custom Prisma Policy:

AWS:VPC-Default AWS Default VPC Check

Description:

Delete the AWS default VPC from offending regions.

Required Permissions:

- ec2:DeleteInternetGateway
- ec2:DeleteNetworkAcl
- ec2:DeleteRouteTable
- ec2:DeleteSecurityGroup
- ec2:DeleteSubnet
- ec2:DeleteVpc
- ec2:DescribeInternetGateways
- ec2:DescribeNetworkAcls
- ec2:DescribeNetworkInterfaces
- ec2:DescribeRouteTables
- ec2:DescribeSecurityGroups
- ec2:DescribeSubnets
- ec2:DescribeVpcs
- ec2:DetachInternetGateway

Sample IAM Policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2Permissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteInternetGateway",
                "ec2:DeleteNetworkAcl",
                "ec2:DeleteRouteTable",
                "ec2:DeleteSecurityGroup",
                "ec2:DeleteSubnet",
                "ec2:DeleteVpc",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeNetworkAcls",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DetachInternetGateway"
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

  vpc_id = alert['resource_id']
  region = alert['region']

  ec2  = session.client('ec2', region_name=region)

  try:
    vpc = ec2.describe_vpcs(VpcIds=[ vpc_id ])
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  else:
    is_default = vpc['Vpcs'][0]['IsDefault']

  # Is this the default VPC?
  if is_default != True:
    print('VPC {} is not the default.'.format(vpc_id))
    return

  # Are there any existing resources?  Since most resources attach an ENI, let's check..
  try:
    eni = ec2.describe_network_interfaces(
            Filters = [
              {
                'Name': 'vpc-id',
                'Values': [ vpc_id ]
              }
            ]
          )['NetworkInterfaces']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  if eni:
    print('VPC {} has existing resources.'.format(vpc_id))
    return

  # Do the work..
  result = delete_igw(ec2, vpc_id)
  result = delete_subs(ec2, vpc_id)
  result = delete_rtbs(ec2, vpc_id)
  result = delete_acls(ec2, vpc_id)
  result = delete_sgps(ec2, vpc_id)
  result = delete_vpc(ec2, vpc_id)

  return


def delete_igw(ec2, vpc_id):
  """
  Detach and delete the internet gateway
  """

  try:
    igw = ec2.describe_internet_gateways(
            Filters = [
              {
                'Name' : 'attachment.vpc-id',
                'Values' : [ vpc_id ]
              }
            ]
          )['InternetGateways']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if igw:
    igw_id = igw[0]['InternetGatewayId']

    try:
      ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    except ClientError as e:
      print(e.response['Error']['Message'])

    try:
      ec2.delete_internet_gateway(InternetGatewayId=igw_id)
    except ClientError as e:
      print(e.response['Error']['Message'])

  return


def delete_subs(ec2, vpc_id):
  """
  Delete the subnets
  """

  try:
    subs = ec2.describe_subnets(
             Filters = [
               {
                 'Name' : 'vpc-id',
                 'Values' : [ vpc_id ]
               }
             ]
           )['Subnets']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if subs:
    for sub in subs:
      sub_id = sub['SubnetId']

      try:
        ec2.delete_subnet(SubnetId=sub_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_rtbs(ec2, vpc_id):
  """
  Delete the route tables
  """

  try:
    rtbs = ec2.describe_route_tables(
             Filters = [
               {
                 'Name' : 'vpc-id',
                 'Values' : [ vpc_id ]
               }
             ]
           )['RouteTables']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if rtbs:
    for rtb in rtbs:
      main = 'false'
      for assoc in rtb['Associations']:
        main = assoc['Main']
      if main == True:
        continue
      rtb_id = rtb['RouteTableId']
        
      try:
        ec2.delete_route_table(RouteTableId=rtb_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_acls(ec2, vpc_id):
  """
  Delete the network access lists (NACLs)
  """

  try:
    acls = ec2.describe_network_acls(
             Filters = [
               {
                 'Name' : 'vpc-id',
                 'Values' : [ vpc_id ]
               }
             ]
           )['NetworkAcls']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if acls:
    for acl in acls:
      default = acl['IsDefault']
      if default == True:
        continue
      acl_id = acl['NetworkAclId']

      try:
        ec2.delete_network_acl(NetworkAclId=acl_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_sgps(ec2, vpc_id):
  """
  Delete any security groups
  """

  try:
    sgps = ec2.describe_security_groups(
             Filters = [
               {
                 'Name' : 'vpc-id',
                 'Values' : [ vpc_id ]
               }
             ]
           )['SecurityGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if sgps:
    for sgp in sgps:
      default = sgp['GroupName']
      if default == 'default':
        continue
      sg_id = sgp['GroupId']

      try:
        ec2.delete_security_group(GroupId=sg_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_vpc(ec2, vpc_id):
  """
  Delete the VPC
  """

  try:
    ec2.delete_vpc(VpcId=vpc_id)
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    print('VPC {} has been deleted.'.format(vpc_id))

  return

