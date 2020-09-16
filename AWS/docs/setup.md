# Setup Guide

## Overview

1. Build the Lambda remediation infrastructure using a CloudFormation template in your Parent AWS account.
2. (Optional) Create an IAM Role and Policy in target (Child) AWS accounts using a CloudFormation template.
3. Integrate Prisma Cloud to send alerts to the Lambda remediation infrastructure.

---

## Step 1 - Create Prisma Cloud Remediation Stack

[![Launch Button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=PrismaRemediation&templateURL=https://prisma-lambda-remediation.s3-us-west-2.amazonaws.com/templates/cloudformation_prisma_template.json)

This CloudFormation stack creates the following resources in the Oregon (us-west-2) region:

- AWS SQS Queue
- AWS IAM Role and Policy to be used by Lambda (See [iam_role_permission.json](../templates/iam_role_permission.json))
- AWS Lambda package containing the runbook scripts to remediate Prisma Cloud alerts.

## Step 2 - Setup IAM Permissions

### Single Account Setup

To remediate a single AWS account, you're done. You can skip this step and move on to step 3, Prisma Cloud Integration.

### Multi Account Setup

The account where the stack is launched (in step 1) can be considered the **Parent** account.  All other accounts are called **Child** or **Target** accounts.

The Parent account will need permission to change/modify AWS resources in your Child account(s).  Next, we'll create a Role that allows the lambda function to perform the remediation.

When you created the CloudFormation stack in step 1, one of the parameters was called `CrossAccountRoleName` (The default value of that parameter is `CrossAccountRemediationRole`). Use the same name when using the CloudFormation template below to create the IAM Role in your Child account(s).

For Multi Account Setup, you will need to create this IAM Role in each Child/Target AWS account.

[![Launch Button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=PrismaChildRemediationRole&templateURL=https://prisma-lambda-remediation.s3-us-west-2.amazonaws.com/templates/cloudformation_role_template.json)

When you get to the **Specify stack details** page, ensure that you replace the `AWSParentAccountId` paramater value to match the [**Parent** account's AWS ID](https://console.aws.amazon.com/billing/home?#/account).

This CloudFormation stack creates the following resources in the Oregon (us-west-2) region:

- AWS IAM Role and Policy to be used by Lambda (See [iam_role_permission.json](../templates/iam_role_permission.json))

## Step 3 - Prisma Cloud Integration

You will need to get the **PrismaRemediationSQSQueue** URL from the Output section of the CloudFormation stack created in step 1.

- Go to the [AWS CloudFormation Dashboard](https://us-west-2.console.aws.amazon.com/cloudformation).
- Click on the Prisma Remediation stack name.
- Select the **Outputs** tab.
- Take note of the **PrismaRemediationSQSQueue** URL.

![Output](../images/cfn_output.jpg)

Create a new Prisma Cloud Integration:

- Login to the Prisma Cloud console.
- From the left-side window pane, slect **Settings**.
- Choose **Integrations**.
- Near the top of the window, click **Add new**.
- Fill out the **Integration name** and **Queue URL** fields, then click Next.  Use the SQS Queue URL from the Output of your CloudFormation stack.
- Click **Test**. You should receive a Success message. If not, double check your URL.
- **Save** your new integration.

At this point, the remediation infrastructure setup is complete.  Let's check...

Check CloudWatchLogs:

- Go to the [AWS Lambda Dashboard](https://us-west-2.console.aws.amazon.com/lambda).
- Click on your Function name.
- Near the top of the next screen, select the **Monitoring** tab.
- Choose **View logs in CloudWatch** near the the top right-hand side of the screen.
- From the new window/tab, click on the latest new log stream.  You should see a test message from Prisma Cloud, sent from your SQS Queue test, similar to the one below.

![Output](../images/logs_output.jpg)

- If you don't see the Prisma Cloud test message, or an error occurred, check out **Further Troubleshooting Lambda**.

Create a new Prisma Cloud Alert rule:

- Login to the Prisma Cloud console.
- From the left-side window pane, slect **Alerts**.
- Choose **Alert rules**.
- Near the top of the window, click **Add new**.
- Fill out the **Alert name** field, then click **Next**.
- Select the account group(s), and **Next**. These are the AWS accounts you're setting up for remediation.
- Choose the Policies you'd like to remediate, then **Next**.
- Enable **Amazon SQS** queue and select the integration you created above.
- Save your new Alert rule.

## Step 4 - (Optional) Further Troubleshooting Lambda

The base remediation package comes with a runbook called **AWS-TEST-001.py** (/runbooks/AWS-TEST-001.py). On the script's comment section, there is a sample SQS message that you can use to test your setup.
- Go to the AWS Lambda Dashboard. https://us-west-2.console.aws.amazon.com/lambda
- Click on the Function name.
- On the left side of the **Test** button, click **Select a test event**.
- Use the sample SQS message, replace `123456789012` account ID with the **Parent** account ID. We can call this event **TargetSelf**.
- Click **Save** and **Test**.

Under **Log Output** Section, you will see:
- `This runbook is invoked by arn:aws:lambda:us-west-2:<parent_account_name>:function:<lambda_function_name>`
followed by the output of `sts.get_caller_identity()`. You will notice that the `Arn` uses the credential from the lambda role.

For multi account setup, repeat all the steps, but specify the **Child/Target** account ID. Under **Log Output** Section, you will see:
- `This runbook is invoked by arn:aws:lambda:us-west-2:<parent_account_name>:function:<lambda_function_name>`
followed by the output of `sts.get_caller_identity()`. You will notice that the `Arn` uses assumed role on another account.

