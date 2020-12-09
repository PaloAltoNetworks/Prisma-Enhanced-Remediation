variable "region" {
  default     = "us-west-2"
  description = "Oregon"
}

variable "source_code_key_path" {
  default     = "aws/lambda/PrismaRemediate-latest.zip"
  description = "Specify the S3 path for the Lambda source code. Uses the latest release by default."
}

variable "cross_account_role_name" {
  default     = "CrossAccountRemediationRole"
  description = "The Role name to be assumed by Lambda for remediation on another account."
}
