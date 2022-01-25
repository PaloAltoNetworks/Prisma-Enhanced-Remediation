"""
Remediate Prisma Policy:
PC-AWS-S3-322  AWS S3 bucket not configured with secure data transport policy
Description:
This policy identifies S3 buckets which are not configured with secure data transport policy. 
It is recommended to add a bucket policy that explicitly denies (Effect: Deny) all access (Action: s3:*) from anybody who browses (Principal: *) to Amazon S3 objects within an Amazon S3 bucket if they are not accessed through HTTPS (aws:SecureTransport: false).
Required permissions:
- s3:PutBucketPolicy
- s3:GetBucketPolicy
Sample IAM Policy:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1507759700000",
      "Effect": "Allow",
      "Action": [
        "s3:PutBucketPolicy",
        "s3:GetBucketPolicy"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}

"""

import boto3
import json
from botocore.exceptions import ClientError


def remediate(session, alert, lambda_context):
  
    bucket_name  = alert['resource_id']
    region = alert['region']
    
    s3_client = session.client('s3', region_name=region)
    

    
    try: 
        result = s3_bucket_ssl_requests_only(bucket_name,s3_client)
    except ClientError as e:
        print(e.response['Error']['Message'])
    except Exception as e:
        raise Exception( "Unexpected error" + e.__str__())    
        return
  


def s3_bucket_ssl_requests_only(bucket_name,s3_client):
    
    """Adds Bucket Policy to force SSL only connections
    """
        
    #defining bucket policy
    bucket_policy = {
              "Id": "ForceSSLOnlyAccess",
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "AllowSSLRequestsOnly",
                  "Action": "s3:*",
                  "Effect": "Deny",
                  "Resource": [
                    "arn:aws:s3:::"+bucket_name,
                    "arn:aws:s3:::"+bucket_name+"/*"
                  ],
                  "Condition": {
                    "Bool": {
                      "aws:SecureTransport": "false"
                    }
                  },
                  "Principal": "*"
                }
              ]
        }
    # Convert the policy to a JSON string
    bucket_policy = json.dumps(bucket_policy)

    # get existing bucket policy
    response = s3_client.get_bucket_policy(Bucket=bucket_name)
        
    #if any bucket policy exists then append the new policy to the old policy
    if (response):
        bucket_policy_new={
              "Sid": "AllowSSLRequestsOnly",
              "Action": "s3:*",
              "Effect": "Deny",
              "Resource": [
                "arn:aws:s3:::"+bucket_name,
                "arn:aws:s3:::"+bucket_name+"/*"
              ],
              "Condition": {
                "Bool": {
                  "aws:SecureTransport": "false"
                }
              },
              "Principal": "*"
            }
            
            
        existing_policy = response['Policy']
        ex_policy=json.loads(existing_policy)
        sub_ex_policy = ex_policy['Statement']
        sub_ex_policy.append(bucket_policy_new)
        ex_policy['Statement']=sub_ex_policy
        print(ex_policy)
        print(' There is a existing Policy, have updated the policy')
         # Convert the policy to a JSON string
        bucket_policy = json.dumps(ex_policy)
        
        
    try:
        response = s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        print('Successful')
    except:
        set_bucket_policy(bucket_name,bucket_policy,s3_client)
            
            
def set_bucket_policy(bucket_name,bucket_policy,s3_client):
   
    """Attempts to set an S3 Bucket Policy. If returned error is Access Denied, 
    then the Public Access Block is removed before placing a new S3 Bucket Policy
    
    Arguments:
        bucket {string} -- S3 Bucket Name
        policy {string} -- S3 Bucket Policy
    
    Returns:
        boolean -- True if S3 Bucket Policy was set
    """
    try:
        # disable Public Access Block
        s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicPolicy": False,
                    "RestrictPublicBuckets": False,
                    },
            )
        print('Here one')
        # put Bucket Policy
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
                # enable Public Access Block
        print('Here two')        
        s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True,
                },
            )
        print('Here three')    
    except:
        print("Could not set SSL requests only policy to S3 Bucket")                
       
        
        
       

