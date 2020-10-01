"""
Remediate Prisma Policy:

AWS:RDS-010 RDS Multi-AZ Check

Description:

Amazon RDS Multi-AZ deployments provide enhanced availability and durability for Database (DB) Instances,
making them a natural fit for production database workloads. When you provision a Multi-AZ DB Instance,
Amazon RDS automatically creates a primary DB Instance and synchronously replicates the data to a standby
instance in a different Availability Zone (AZ). Each AZ runs on its own physically distinct, independent
infrastructure, and is engineered to be highly reliable. In case of an infrastructure failure, Amazon RDS
performs an automatic failover to the standby (or to a read replica in the case of Amazon Aurora), so that
you can resume database operations as soon as the failover is complete. Since the endpoint for your DB
instance remains the same after a failover, your application can resume database operation without the
need for manual administrative intervention.

Required Permissions:

- rds:DescribeDBInstances
- rds:ModifyDBInstance

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RDSPermissions",
      "Action": [
        "rds:DescribeDBInstances",
        "rds:ModifyDBInstance"
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

  resource_id = alert['resource_id']
  region      = alert['region']

  rds = session.client('rds', region_name=region)

  try:
    db_instance = rds.describe_db_instances(
      Filters = [
        {
          'Name': 'dbi-resource-id',
          'Values': [ resource_id ]
        }
      ]
    )['DBInstances']

  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  try:
    multi_az = db_instance[0]['MultiAZ']
  except (KeyError, IndexError):
    pass

  else:

    if multi_az != True:

      instance_id = db_instance[0]['DBInstanceIdentifier']

      try:
        result = rds.modify_db_instance(
          DBInstanceIdentifier = instance_id,
          ApplyImmediately = True,
          MultiAZ = True
        )
      except ClientError as e:
        print(e.response['Error']['Message'])
      else:
        print('Enabled \'MultiAZ\' for RDS instance {}.'.format(instance_id))

  return

