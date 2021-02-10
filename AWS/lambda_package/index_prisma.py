from __future__ import print_function
from importlib import import_module
from botocore.exceptions import ClientError
import boto3
import json
import os


# Prisma Cloud ID to old Evident ID

runbook_lookup = {
    'c2b84f89-7ec8-473e-a6af-404feeeb96c5' : 'AWS-CLT-002',
    '0d07ac51-fbfe-44fe-8edb-3314c9995ee0' : 'AWS-CLT-004',
    '962e0daa-3c2d-4d79-9a5f-e0bf8fd4bb3b' : 'AWS-CLT-004',
    '38e3d3cf-b694-46ec-8bd2-8f02194b5040' : 'AWS-CLT-005',
    'b76ad441-e715-4fd0-bbc3-cd3b2bee34bf' : 'AWS-CLT-006',
    '617b9138-584b-4e8e-ad15-7fbabafbed1a' : 'AWS-EC2-002',
    '519456f2-f9eb-407b-b32d-064f1ac7f0ca' : 'AWS-EC2-003',
    'b82f90ce-ed8b-4b49-970c-2268b0a6c2e5' : 'AWS-EC2-004',
    '65daa6a0-e040-434e-aca3-9d5765c96e7c' : 'AWS-EC2-010',
    '3b642d25-4534-487a-9399-c2622754ecb5' : 'AWS-EC2-010',
    '760f2823-997e-495f-a538-5fb073c0ee78' : 'AWS-EC2-010',
    'ab7f8eda-18ab-457c-b5d3-fd4f53c722bc' : 'AWS-EC2-010',
    '8dd9e369-0c09-4477-97a2-ff0d50507fe2' : 'AWS-EC2-010',
    '89cbc2f1-fcb0-48b9-be71-4cbe2d18a5f7' : 'AWS-EC2-010',
    '14d10ad2-51df-4b07-be69-e94951cc7067' : 'AWS-EC2-010',
    'cdcd663c-e9c9-4472-9779-e5f38751524a' : 'AWS-EC2-010',
    'c2074d5a-aa28-4dde-90c1-82f528cec55e' : 'AWS-EC2-010',
    '6eaf6455-1659-4c4b-bff5-c8c7b0fda201' : 'AWS-EC2-010',
    '81a2200a-c63e-4860-85a0-b54eaa581135' : 'AWS-EC2-036',
    '2378dbf4-b104-4bda-9b05-7417affbba3f' : 'AWS-EC2-038',
    '566686e8-0581-4df5-ae22-5a901ed37b58' : 'AWS-EC2-039',
    '7c714cb4-3d47-4c32-98d4-c13f92ce4ec5' : 'AWS-EC2-042',
    '7eb7f61e-df59-42d4-8236-7d012f278fa6' : 'AWS-ELB-009',
    '551ee7ba-edb6-468e-a018-8774da9b1e85' : 'AWS-ELB-012',
    'b675c604-e886-43aa-a60f-a9ad1f3742d3' : 'AWS-ELB-013',
    'f2a2bcf1-2966-4cb5-9230-bd39c9903a02' : 'AWS-ELB-015',
    '7ca5af2c-d18d-4004-9ad4-9c1fbfcab218' : 'AWS-IAM-015',
    'd9b86448-11a2-f9d4-74a5-f6fc590caeef' : 'AWS-IAM-016',
    '497f7e2c-b702-47c7-9a07-f0f6404ac896' : 'AWS-KMS-001',
    '1bb6005a-dca6-40e2-b0a6-24da968c0808' : 'AWS-RDS-005',
    'a707de6a-11b7-478a-b636-5e21ee1f6162' : 'AWS-RDS-007',
    'c5305272-a732-4e8e-8427-6a9701cd2a6f' : 'AWS-RDS-010',
    '9dd6cc35-1855-48c8-86ba-0e1818ce11e2' : 'AWS-RDS-011',
    'd65fd313-1c5c-42a1-98b2-a73bdeda19a6' : 'AWS-REDSHIFT-001',
    '89ea62c1-3845-4134-b337-cc82203b8ff9' : 'AWS-SSS-001',
    '43c42760-5283-4bc4-ac43-a80e58c4139f' : 'AWS-SSS-008',
    '4daa435b-fa46-457a-9359-6a4b4a43a442' : 'AWS-SSS-009',
    '7913fcbf-b679-5aac-d979-1b6817becb22' : 'AWS-SSS-014',
    '630d3779-d932-4fbf-9cce-6e8d793c6916' : 'PC-AWS-S3-29',
    '49f4760d-c951-40e4-bfe1-08acaa17672a' : 'AWS-VPC-020',
    '11111111-1111-1111-1111-111111111111' : 'AWS-TEST-001'
}


def parse_alert_message(sqs_message):
    """ 
     *** Extract Prisma Cloud SQS message ***

    returns dict:
        'error' : will be None if the message is parsed successfully. Otherwise, it contains the error message
        'data'  : contains the parsed alert, or None if the alert message isn't parsed successfully
            region           region of the resource referenced in the alert
            resource_id      AWS resource ID
            alert_id         Prisma Cloud alert ID
            account
                name
                account_number
            runbook_id       Convert Prisma Cloud policy ID to runbook ID
            metadata         Metadata details of the alert
    """

    try:
        alert = json.loads(sqs_message)

        # Check for Prisma Cloud test notification
        if alert['alertId'] == 'P-0':
            return {'error': "Prisma Cloud Test Notification", 'data': alert['alertId']}
            
        # Only remediate AWS
        #if alert['cloudType'] != 'aws':
        #    return {'error': "Cloud not AWS", 'data': alert}

        parsed_alert = {
            'region'             : alert['resourceRegionId'],
            'resource_id'        : alert['resourceId'],
            'alert_id'           : alert['alertId'],
            'account': {
                'name'           : alert['accountName'],
                'account_number' : alert['accountId']
            },
            'runbook_id'         : None,
            'metadata'           : alert['resource']
        }

        # Default region set to us-east-1 if we receive "global" region
        if parsed_alert['region'] == 'global':
            parsed_alert['region'] = 'us-east-1'

        if alert['policyId'] in runbook_lookup:
            parsed_alert['runbook_id'] = runbook_lookup[alert['policyId']]
            return {'error': None, 'data': parsed_alert}
        else:
            return {'error': "Runbook not found", 'data': parsed_alert}

    except Exception as e:
        return {'error': str(e), 'data': None}


def get_credentials(account_id):
    """
    Using STS assume role to obtain the temporary credentials of another AWS account

    returns dict:
        'error'    : None if credentials is acquired successfully. Otherwise, it contains error message
        'data'     : Contains the credentials, or none if an error is encountered
            AccessKeyId
            Expiration
            SecretAccessKey
            SessionToken
    """

    cross_account_role_name = os.getenv('CROSS_ACCOUNT_ROLE_NAME', None)

    if cross_account_role_name == None:
        return {'error': 'Lambda env variable CROSS_ACCOUNT_ROLE_NAME not specified.', 'data': None}

    try:
        resp = boto3.client('sts').assume_role(
            RoleArn = 'arn:aws:iam::{0}:role/{1}'.format(account_id, cross_account_role_name),
            RoleSessionName = 'PrismaRemediation'
            )

        return {'error': None, 'data': resp['Credentials']}
    except ClientError as e:
        error = 'Failed to assume role. Error code: {0}'.format(e.response['Error']['Code'])
        return {'error': error, 'data': None}


def lambda_handler(event, context):
    """
    Entry point which is invoked by Lambda
    """

    print("#### Received {} record(s) ####".format(len(event['Records'])))

    for record in event['Records']:
        parsed_alert = parse_alert_message(record['body'])

        if parsed_alert['data'] == 'P-0':
            print(parsed_alert['error'])
        else:
            
            if parsed_alert['error'] is not None:
                print('Error in SQS record. Raw message:', record)
                raise Exception(parsed_alert['error'])
            else:
                parsed_alert = parsed_alert['data']

            # Check to see if the remediation runbook exists 
            try:
                runbook = import_module('runbooks.' + parsed_alert['runbook_id'])
            except Exception as e:
                message = 'Cannot import/find runbook for {0} ({1}). Error: {2}'.format(parsed_alert['runbook_id'], parsed_alert['policy_id'], str(e))
                raise Exception(message)

            # If the resource is on another account, get the temporary credentials
            self_account_id = context.invoked_function_arn.split(":")[4]
            if parsed_alert['account']['account_number'] == self_account_id:
                session = boto3.Session(region_name = parsed_alert['region'])
            else:
                credentials = get_credentials(parsed_alert['account']['account_number'])
                if credentials['error'] is None:
                    session = boto3.Session(
                        region_name = parsed_alert['region'],
                        aws_access_key_id = credentials['data']['AccessKeyId'],
                        aws_secret_access_key = credentials['data']['SecretAccessKey'],
                        aws_session_token = credentials['data']['SessionToken']
                        )
                else:
                    raise Exception(credentials['error'])
                
            # Finally, execute the runbook
            print('Remediation for Prisma Cloud alert: ', parsed_alert['alert_id'])
            print('Alert detail: ', parsed_alert)
            print('Executing runbook; ', parsed_alert['runbook_id'], '...')

            runbook.remediate(session, parsed_alert, context)
