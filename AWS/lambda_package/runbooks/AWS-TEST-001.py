import boto3

"""

Use the following Test Event 

{"Records":[{"EventVersion":"1.0","EventSubscriptionArn":"arn:aws:sns:EXAMPLE","EventSource":"aws:sns","Sns":{"SignatureVersion":"1","Timestamp":"1970-01-01T00:00:00.000Z","Signature":"EXAMPLE","SigningCertUrl":"EXAMPLE","MessageId":"95df01b4-ee98-5cb9-9903-4c221d41eb5e","Message":"{\"data\":{\"id\":\"111111111\",\"type\":\"alerts\",\"attributes\":{\"created_at\":\"2020-12-20T20:33:06.000Z\",\"status\":\"fail\",\"risk_level\":\"medium\",\"resource\":\"resource_id_here\",\"ended_reason\":null,\"replaced_by_id\":null,\"replaced_by_status\":null,\"updated_at\":\"2020-01-29T23:28:05.000Z\",\"started_at\":\"2020-12-20T20:33:06.000Z\",\"ended_at\":null}},\"included\":[{\"id\":\"0\",\"type\":\"external_accounts\",\"attributes\":{\"created_at\":\"1987-07-21T00:44:24.000Z\",\"name\":\"My First ESP External Accounts\",\"updated_at\":\"1987-01-18T08:45:12.000Z\",\"provider\":\"amazon\",\"arn\":\"arn:aws:iam::123456789012:role/ESP-Role-2\",\"account\":\"123456789012\",\"external_id\":\"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\",\"cloudtrail_name\":\"Cloudtrail Name\"}},{\"id\":\"6\",\"type\":\"regions\",\"attributes\":{\"code\":\"us_east_1\",\"name\":null,\"created_at\":\"2014-06-05T23:42:37.000Z\",\"updated_at\":\"2014-06-05T23:42:37.000Z\",\"provider\":\"amazon\"}},{\"id\":\"0\",\"type\":\"signatures\",\"attributes\":{\"created_at\":\"2017-12-15T20:29:49.000Z\",\"description\":\"Sample Signature\",\"identifier\":\"AWS:TEST-001\",\"name\":\"Remediation Test\",\"resolution\":\"nothing\",\"risk_level\":\"medium\",\"updated_at\":\"2017-12-20T18:59:02.000Z\"}},{\"id\":\"0\",\"type\":\"metadata\",\"attributes\":{\"data\":{\"details\":{\"some\":\"alert details\"}}}}]}","MessageAttributes":{"Test":{"Type":"String","Value":"TestString"},"TestBinary":{"Type":"Binary","Value":"TestBinary"}},"Type":"Notification","UnsubscribeUrl":"EXAMPLE","TopicArn":"arn:aws:sns:EXAMPLE","Subject":"TestInvoke"}}]}

To test standalone account remediation, replace 123456789012 account ID with the standalone AWS account ID
To test remediating alert from another account, replace 123456789012 account ID with another AWS account to assume role

"""

def remediate(session, alert, lambda_context):
    print('This runbook is invoked by {}'.format(lambda_context.invoked_function_arn))
    print('Runbook session Details:')

    client = session.client('sts')

    resp = client.get_caller_identity()
    print(resp)
    return 0
