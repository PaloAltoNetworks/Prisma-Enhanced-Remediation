"""
Remediate Prisma Policy:

AWS:RDS-007 RDS Snapshot with Public Permissions

Description:

If you set DB Snapshot Visibility to Public, all AWS accounts can restore a DB instance from your
DB snapshot and have access to your data. Best practice is to not share any DB snapshots that contain
private information as Public.

Required Permissions:

- rds:DescribeDBSnapshotAttributes
- rds:ModifyDBSnapshotAttribute

Sample IAM Policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RDSPermissions",
            "Effect": "Allow",
            "Action": [
                "rds:DescribeDBSnapshotAttributes",
                "rds:ModifyDBSnapshotAttribute"
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

  snapshot_id = alert['resource_id']
  region = alert['region']

  rds = session.client('rds', region_name=region)

  try:
    attributes = rds.describe_db_snapshot_attributes(DBSnapshotIdentifier=snapshot_id)['DBSnapshotAttributesResult']['DBSnapshotAttributes']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return
    
  public = False

  for attrib in attributes:
    if attrib['AttributeName'] == 'restore':
      try:
        if (attrib['AttributeValues'][0] == 'all'):
          public = True
      except IndexError:
          continue
    else:
      print('Unable to find public attribute for RDS snapshot {}.'.format(snapshot_id))

  if public == True:

    snap_args = {
      'DBSnapshotIdentifier' : snapshot_id,
      'AttributeName' : 'restore',
      'ValuesToRemove' : [ 'all' ]
    }

    try:
      results = rds.modify_db_snapshot_attribute(**snap_args)

      print('Removed public attribute from RDS snapshot {}.'.format(snapshot_id))

    except ClientError as e:
      print(e.response['Error']['Message'])

  return
