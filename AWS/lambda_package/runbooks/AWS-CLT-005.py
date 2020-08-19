"""
Remediate Prisma Policy:

AWS:CLT-005 Log file validation not enabled for CloudTrail Log File

Description:

The CloudTrail log file validation creates a digest for each log file written to S3. These digests
can be used to determine whether a log file was changed, deleted, or unchanged after CloudTrail delivered
the file.

Required Permissions:

- cloudtrail:DescribeTrails
- cloudtrail:UpdateTrail

Sample IAM Policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudTrailPermissions",
            "Effect": "Allow",
            "Action": [
                "cloudtrail:DescribeTrails",
                "cloudtrail:UpdateTrail"
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
  Main Function invoked by index.py
  """

  trail_name  = alert['resource_id']
  region      = alert['region']

  clt = session.client('cloudtrail', region_name=region)

  try:
    trail = clt.describe_trails(trailNameList=[ trail_name ], includeShadowTrails=False)['trailList']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  if trail[0]['LogFileValidationEnabled'] != True:
    result = enable_validation(clt, trail_name)

  return


def enable_validation(clt, trail_name):
  """
  Enable CloudTrail Log File Validation
  """

  try:
    result = clt.update_trail(Name=trail_name, EnableLogFileValidation=True)
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Enabled log file validation for Trail {}.'.format(trail_name))

  return

