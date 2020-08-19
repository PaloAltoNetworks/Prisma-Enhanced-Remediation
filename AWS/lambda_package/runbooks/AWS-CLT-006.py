"""
Remediate Prisma Policy:

AWS:CLT-006 S3 Bucket ACL allows public access to CloudTrail logs

Description:

It is recommended that the bucket policy or access control list (ACL) applied to the S3 bucket
that stores CloudTrail logs prevents public access. Allowing public access to CloudTrail log content
may aid an adversary in identifying weaknesses in the affected account's use or configuration.

Required Permissions:

- cloudtrail:DescribeTrails
- s3:GetBucketAcl
- s3:PutBucketAcl

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudTrailPermissions",
      "Action": [
        "cloudtrail:DescribeTrails"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "S3Permissions",
      "Action": [
        "s3:GetBucketAcl",
        "s3:PutBucketAcl"
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

  trail_name  = alert['resource_id']
  region      = alert['region']

  clt = session.client('cloudtrail', region_name=region)
  s3  = session.client('s3', region_name=region)

  try:
    trail = clt.describe_trails(trailNameList=[ trail_name ], includeShadowTrails=False)['trailList']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  try:
    bucket_name = trail[0]['S3BucketName']
  except (IndexError, KeyError):
    print('Could not find S3 bucket for Trail {}.'.format(trail_name))
    return

  try:
    bucket_acl = s3.get_bucket_acl(Bucket=bucket_name)
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  new_bucket_acl = {}
  new_bucket_acl['Owner'] = bucket_acl['Owner']

  new_grants = []
  public = False
  
  for grant in bucket_acl['Grants']:
    try:
      grant_type = grant['Grantee']['Type']
      grant_uri  = grant['Grantee']['URI']
    except KeyError:
      new_grants.append(grant)
      continue

    if ((grant_type == 'Group' and 'AllUsers' in grant_uri) or
        (grant_type == 'Group' and 'AuthenticatedUsers' in grant_uri)):
      public = True
    else:
      new_grants.append(grant)

  new_bucket_acl['Grants'] = new_grants

  # Remediate
  if public == True:
    result = remove_public_acl(s3, bucket_name, new_bucket_acl, trail_name)
    
  return


def remove_public_acl(s3, bucket_name, new_bucket_acl, trail_name):
  """
  Remove S3 Bucket Public ACL Policy
  """

  try:
    result = s3.put_bucket_acl(
      AccessControlPolicy = new_bucket_acl,
      Bucket = bucket_name
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('S3 bucket {} ACL policy, removed public access for Trail {}.'.format(bucket_name, trail_name))

  return

