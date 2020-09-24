import boto3

"""
Remediate Prisma Policy:

AWS:IAM-016 Custom IAM Policy Grants Too Many Privileges

Description:

Best practice is to not create a custom IAM policy with administrator access. 
If administrator access grant is needed, use the default AdministratorAccess policy

Required permissions:

- iam:CreatePolicyVersion

Sample IAM Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1507759700000",
      "Effect": "Allow",
      "Action": [
        "iam:CreatePolicyVersion"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}

Remediation result:
- Modify custom policy with a placeholder policy with minimum access
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sts:getCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}

"""

def remediate(session, alert, lambda_context):

    resource_id = alert['resource_id']

    new_policy = "{\n    \"Version\": \"2012-10-17\",\n    \"Statement\": [\n        {\n            \"Sid\": \"VisualEditor0\",\n            \"Effect\": \"Allow\",\n            \"Action\": [\n                \"sts:getCallerIdentity\"\n            ],\n            \"Resource\": \"*\"\n        }\n    ]\n}"

    client = session.client('iam')

    print('Modifying policy: {}'.format(alert['resource_id']))
    
    try:
        resp = client.create_policy_version(
            PolicyArn = resource_id,
            PolicyDocument = new_policy,
            SetAsDefault = True
            )

    except Exception as e:
        raise e
    
    return 0
