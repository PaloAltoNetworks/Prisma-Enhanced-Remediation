"""
Remediate Prisma Policy:

AWS:SSS-008 S3 Bucket has Global ACL Permissions enabled

Description:

Remove the existence of Global ACL permissions on S3 Bucket for the All Users and Authenticated Users groups.

Required Permissions:

- s3:GetBucketAcl
- s3:PutBucketAcl

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
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

  bucket_name  = alert['resource_id']
  region       = alert['region']

  s3 = session.client('s3', region_name=region)

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
    result = remove_public_acl(s3, bucket_name, new_bucket_acl)
    
  return


def remove_public_acl(s3, bucket_name, new_bucket_acl):
  """
  Remove S3 Bucket Global ACL Policy
  """

  try:
    result = s3.put_bucket_acl(
      AccessControlPolicy = new_bucket_acl,
      Bucket = bucket_name
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print('Global access removed from S3 bucket {} ACL policy.'.format(bucket_name))

  return

