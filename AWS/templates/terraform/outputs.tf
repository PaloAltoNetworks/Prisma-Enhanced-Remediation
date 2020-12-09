output "PrismaRemediationLambda" {
  value = aws_lambda_function.lambda_function.function_name
}

output "PrismaRemediationSQSQueue" {
  value = aws_sqs_queue.prisma_remediation_queue.id
}

data "aws_caller_identity" "current" {}

output "PrismaRemediationParentId" {
  value = data.aws_caller_identity.current.account_id
}

output "PrismaCrossAccountIAMRole" {
  value = var.cross_account_role_name
}
