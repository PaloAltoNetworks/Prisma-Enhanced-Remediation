import boto3

"""

Use the following Test Event to test Lambda:

{
  "Records": [
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
      "receiptHandle": "MessageReceiptHandle",
      "body": "{\"sender\": \"Test Notification\",\"sentTs\": 1600293588125,\"alertId\": \"T-0\",\"policyId\": \"11111111-1111-1111-1111-111111111111\",\"resourceRegionId\": \"us-west-2\",\"resourceId\": \"i-11111111111111111\",\"accountName\": \"Test\",\"accountId\": \"123456789012\",\"resource\": \"This is a test message.\"}",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "SenderId": "123456789012",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      },
      "messageAttributes": {},
      "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
      "awsRegion": "us-west-2"
    } 
  ]   
}  

To test; Replace "123456789012" in the accountId field, with your AWS account ID.

Note: The "body" field must be a single line.

"""

def remediate(session, alert, lambda_context):
    print('This runbook is invoked by {}'.format(lambda_context.invoked_function_arn))
    print('Runbook session Details:')

    client = session.client('sts')

    resp = client.get_caller_identity()
    print(resp)
    return 0
