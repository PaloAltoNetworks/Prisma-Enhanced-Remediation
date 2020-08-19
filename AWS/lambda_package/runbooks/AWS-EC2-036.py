"""
Remediate Prisma Policy:

AWS:EC2-036 Public AMI Detected

Description:

Publicly shared AMIs pose a risk in exposing sensitive data.

Required Permissions:

- ec2:DescribeImageAttribute
- ec2:ModifyImageAttribute

Sample IAM Policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2Permissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeImageAttribute",
                "ec2:ModifyImageAttribute"
            ],
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

  image_id = alert['resource_id']
  region   = alert['region']

  ec2  = session.client('ec2', region_name=region)

  try:
    attribute = ec2.describe_image_attribute(ImageId=image_id, Attribute='launchPermission')
    launch_permissions = attribute['LaunchPermissions']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  # Check for 'Public' permissions
  if launch_permissions == [{'Group': 'all'}]:
    response = set_ami_to_private(ec2, image_id)

  return


def set_ami_to_private(ec2, image_id):
  """
  Toggle the AMI to private from public by removing 
  {'Group': 'all'} from AMI's LaunchPermissions
  """

  try:
    response = ec2.modify_image_attribute(
      ImageId = image_id,
      Attribute = 'launchPermission',
      LaunchPermission = {
        'Remove': [{'Group': 'all'}]
      }
    )

    print('Removed "Public" LaunchPermission from AMI {}.'.format(image_id))

  except ClientError as e:
    print(e.response['Error']['Message'])

  return

