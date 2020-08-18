"""
Remediate Prisma Policy:

AWS:EC2-042 EBS Snapshot set with Public Permissions

Description:

To avoid exposing personal and sensitive data, we recommend against sharing your EBS snapshots with
all AWS accounts.

Required Permissions:

- ec2:DescribeSnapshotAttribute
- ec2:ModifySnapshotAttribute

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EC2Permissions",
      "Action": [
        "ec2:DescribeSnapshotAttribute",
        "ec2:ModifySnapshotAttribute"
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

  snapshot_id = alert['resource_id']
  region = alert['region']

  ec2 = session.client('ec2', region_name=region)

  try:
    snap_attrib = ec2.describe_snapshot_attribute(
    Attribute = 'createVolumePermission',
    SnapshotId = snapshot_id
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  vol_perms = snap_attrib['CreateVolumePermissions'] if ('CreateVolumePermissions' in snap_attrib) else ''

  public = False

  for perm in vol_perms:
    try:
      if perm['Group'] == 'all':
        public = True
    except KeyError:
      continue

  if public == True:
    result = remove_pub_snapshot_attrib(ec2, snapshot_id) 

  return


def remove_pub_snapshot_attrib(ec2, snapshot_id):
  """
  Remove Public Snaphot Attribute
  """

  try:
    result = ec2.modify_snapshot_attribute(
      Attribute = 'createVolumePermission',
      GroupNames = [
        'all',
      ],
      OperationType = 'remove',
      SnapshotId = snapshot_id
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Removed "Public" attribute from EBS snapshot {}.'.format(snapshot_id))

  return

