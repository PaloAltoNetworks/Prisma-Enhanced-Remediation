variable "region" {
  default     = "us-west-2"
  description = "Oregon"
}

variable "aws_parent_account_id" {
  default     = "123456789012"
  description = "The parent remediation AWS Account ID."
}

variable "cross_account_role_name" {
  default     = "CrossAccountRemediationRole"
  description = "The Role name to be assumed by Lambda for remediation on another account."
}
