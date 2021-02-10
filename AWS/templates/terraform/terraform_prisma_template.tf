provider "aws" {
  region = var.region
}

terraform {
  backend "s3" {}
}

resource "aws_sqs_queue" "prisma_remediation_queue" {
  name                       = "PrismaRemediationQueue"
  visibility_timeout_seconds = 1800

  tags = {
    Name = "Prisma Remediation"
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "PrismaRemediationRole"
  assume_role_policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Sid": "PrismaRemedyLambda",
          "Effect": "Allow",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          }
        }
      ]
    }
EOF

  tags = {
    Name = "Prisma Remediation"
  }
}

resource "aws_iam_role_policy" "lambda_policy" {
  name   = "PrismaRemediationPolicy"
  role   = aws_iam_role.lambda_role.id
  policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "sts:GetCallerIdentity",
            "s3:CreateBucket",
            "s3:GetBucketLogging",
            "s3:PutBucketLogging",
            "ec2:DescribeSecurityGroups",
            "ec2:RevokeSecurityGroupIngress",
            "ec2:AuthorizeSecurityGroupIngress",
            "iam:AttachRolePolicy",
            "iam:CreateRole",
            "iam:CreateUser",
            "iam:GetPolicy",
            "cloudtrail:DescribeTrails",
            "s3:GetBucketAcl",
            "s3:PutBucketAcl",
            "ec2:CreateSnapshot",
            "ec2:DescribeSnapshots",
            "ec2:DeleteSecurityGroup",
            "lambda:ListFunctions",
            "rds:DescribeDBSnapshotAttributes",
            "rds:ModifyDBSnapshotAttribute",
            "iam:PutRolePolicy",
            "iam:GetRole",
            "logs:CreateLogGroup",
            "logs:PutRetentionPolicy",
            "ec2:CreateFlowLogs",
            "ec2:RevokeSecurityGroupEgress",
            "s3:PutBucketVersioning",
            "ec2:DescribeAddresses",
            "ec2:ReleaseAddress",
            "s3:PutEncryptionConfiguration",
            "kms:EnableKeyRotation",
            "logs:DescribeLogGroups",
            "cloudtrail:UpdateTrail",
            "ec2:DescribeImageAttribute",
            "ec2:ModifyImageAttribute",
            "cloudformation:DescribeStacks",
            "cloudformation:UpdateTerminationProtection",
            "s3:PutBucketPolicy",
            "config:PutConfigurationRecorder",
            "config:PutDeliveryChannel",
            "config:StartConfigurationRecorder",
            "rds:DescribeDBInstances",
            "rds:ModifyDBInstance",
            "ec2:DescribeSnapshotAttribute",
            "ec2:ModifySnapshotAttribute",
            "s3:GetBucketLocation",
            "kms:CreateAlias",
            "kms:CreateKey",
            "elasticloadbalancing:DescribeLoadBalancerAttributes",
            "elasticloadbalancing:ModifyLoadBalancerAttributes",
            "s3:PutObject",
            "s3:PutBucketPublicAccessBlock",
            "elasticloadbalancing:DescribeLoadBalancers",
            "iam:UpdateAccountPasswordPolicy",
            "iam:GetAccessKeyLastUsed",
            "iam:UpdateAccessKey",
            "iam:CreatePolicyVersion",
            "kms:DescribeKey",
            "kms:DisableKey",
            "kms:CancelKeyDeletion",
            "redshift:DescribeClusters",
            "redshift:ModifyCluster",
            "ec2:DeleteInternetGateway",
            "ec2:DeleteNetworkAcl",
            "ec2:DeleteRouteTable",
            "ec2:DeleteSubnet",
            "ec2:DeleteVpc",
            "ec2:DescribeInternetGateways",
            "ec2:DescribeNetworkAcls",
            "ec2:DescribeNetworkInterfaces",
            "ec2:DescribeRouteTables",
            "ec2:DescribeSubnets",
            "ec2:DescribeVpcs",
            "ec2:DetachInternetGateway",
            "iam:PassRole"
          ],
          "Resource": [
            "*"
          ],
          "Effect": "Allow",
          "Sid": "PrismaRemediation"
        }
      ]
    }
EOF

  depends_on = [aws_iam_role.lambda_role]
}

resource aws_iam_role_policy "assume_role_policy" {
  name   = "AssumeRolePolicy"
  role   = aws_iam_role.lambda_role.id
  policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Resource": "*",
          "Effect": "Allow"
        }
      ]
    }
EOF

  depends_on = [aws_iam_role.lambda_role]
}

resource "aws_iam_role_policy_attachment" "aws_lambda_SQS_queue_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
  role       = aws_iam_role.lambda_role.id

  depends_on = [aws_iam_role.lambda_role]
}

resource "aws_lambda_function" "lambda_function" {
  function_name = "PrismaRemediation"
  description   = "Prisma Remediation Lambda function"
  s3_bucket     = "prisma-enhanced-remediation-${var.region}"
  s3_key        = var.source_code_key_path

  environment {
    variables = {
      CROSS_ACCOUNT_ROLE_NAME = var.cross_account_role_name
    }
  }

  handler       = "index_prisma.lambda_handler"
  role          = aws_iam_role.lambda_role.arn
  timeout       = 300
  runtime       = "python3.6"

  tags = {
    Name = "Prisma Remediation"
  }

  depends_on = [aws_iam_role.lambda_role]
}

resource "aws_lambda_event_source_mapping" "lambda_trigger" {
  enabled          = true
  batch_size       = 10
  event_source_arn = aws_sqs_queue.prisma_remediation_queue.arn
  function_name    = aws_lambda_function.lambda_function.arn

  depends_on = [aws_sqs_queue.prisma_remediation_queue, aws_lambda_function.lambda_function]
}
