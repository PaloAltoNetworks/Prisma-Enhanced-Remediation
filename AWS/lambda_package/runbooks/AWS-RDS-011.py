"""
Remediate Prisma Policy:

AWS:RDS-011 RDS Minor Upgrades Enabled

Description:

When Amazon Relational Database Service (Amazon RDS) supports a new version of a database engine, you can
upgrade your DB instances to the new version. There are two kinds of upgrades: major version upgrades and
minor version upgrades. Minor upgrades helps maintain a secure and stable RDS with minimal impact on the
application. For this reason, we recommend that your automatic minor upgrade is enabled. Minor version
upgrades only occur automatically if a minor upgrade replaces an unsafe version, such as a minor upgrade
that contains bug fixes for a previous version.

Note: Changing this parameter doesn't result in an outage except in the following case and the change is
asynchronously applied as soon as possible. An outage will result if this parameter is set to true during
the maintenance window, and a newer minor version is available, and RDS has enabled auto patching for that
engine version.

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
  Main Function invoked by index.py
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
    minor_upgrade = db_instance[0]['AutoMinorVersionUpgrade']
  except (KeyError, IndexError):
    pass

  else:

    if minor_upgrade != True:

      instance_id = db_instance[0]['DBInstanceIdentifier']

      try:
        result = rds.modify_db_instance(
          DBInstanceIdentifier = instance_id,
          AutoMinorVersionUpgrade = True
        )
      except ClientError as e:
        print(e.response['Error']['Message'])
      else:
        print('Enabled \'AutoMinorVersionUpgrade\' for RDS instance {}.'.format(instance_id))

  return

