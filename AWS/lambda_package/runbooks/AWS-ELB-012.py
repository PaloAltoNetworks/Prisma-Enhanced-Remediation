"""
Remediate Prisma Policy:

AWS:ELB-012 ELB (Classic) Cross-Zone Load Balancing

Description:

Cross-zone load balancing reduces the need to maintain equivalent numbers of instances in each enabled
Availability Zone, and improves your application's ability to handle the loss of one or more instances.
However, we still recommend that you maintain approximately equivalent numbers of instances in each
enabled Availability Zone for higher fault tolerance.

Required Permissions:

- elasticloadbalancing:DescribeLoadBalancerAttributes
- elasticloadbalancing:ModifyLoadBalancerAttributes

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ELBPermissions",
      "Action": [
        "elasticloadbalancing:DescribeLoadBalancerAttributes",
        "elasticloadbalancing:ModifyLoadBalancerAttributes"
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

  arn      = alert['resource_id']
  elb_name = arn.split('/')[1]
  region   = alert['region']

  elb = session.client('elb', region_name=region)

  try:
    attribs = elb.describe_load_balancer_attributes(LoadBalancerName=elb_name)['LoadBalancerAttributes']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  cross_zone = attribs['CrossZoneLoadBalancing']

  if cross_zone['Enabled'] != True:
    result = enable_cross_zone(elb, elb_name)

  return


def enable_cross_zone(elb, elb_name):
  """
  Enable ELB (Classic) Cross-Zone Load Balancing
  """

  try:
    result = elb.modify_load_balancer_attributes(
      LoadBalancerName = elb_name,
      LoadBalancerAttributes = {
        'CrossZoneLoadBalancing': {
          'Enabled': True
        }
      }
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Enabled Cross-Zone Load Balancing for ELB {}.'.format(elb_name))

  return

