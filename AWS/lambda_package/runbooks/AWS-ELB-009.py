"""
Remediate Prisma Policy:

AWS:ELB-009 ELB (Classic) Connection Draining

Description:

Enable connection draining, and then specify a maximum time for the Load Balancer to keep connections alive
before reporting the instance as de-registered. The maximum timeout value can be set between 1 and 3,600
seconds (the default is 300 seconds). When the maximum time limit is reached, the load balancer forcibly
closes connections to the de-registering instance.

If an instance becomes unhealthy, the load balancer reports the instance state as OutOfService. If there are
in-flight requests made to the unhealthy instance, they are completed.

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
  Main Function invoked by index_prisma.py
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

  draining = attribs['ConnectionDraining']

  if draining['Enabled'] != True:
    result = enable_conn_draining(elb, elb_name)

  return


def enable_conn_draining(elb, elb_name):
  """
  Enable ELB (Classic) Connection Draining
  """

  try:
    result = elb.modify_load_balancer_attributes(
      LoadBalancerName = elb_name,
      LoadBalancerAttributes = {
        'ConnectionDraining': {
          'Enabled': True,
          'Timeout': 300
        }
      }
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Enabled Connection Draining for ELB {}.'.format(elb_name))

  return

