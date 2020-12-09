## Using Terraform

**Authentication**

AWS [Authentication](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

Recommended:
```
$ export AWS_ACCESS_KEY_ID="anaccesskey"
$ export AWS_SECRET_ACCESS_KEY="asecretkey"
$ export AWS_DEFAULT_REGION="us-west-2"
```

**Configuration**

Setup your [Backend Configuration](https://www.terraform.io/docs/backends/config.html#backend-configuration-file)

Initialize your working directory containing Terraform configuration files.
```
terraform init -backend-config="prisma.config"
```

Update the variables as needed.

Default tfvars:
```
region                  = "us-west-2"
source_code_key_path    = "aws/lambda/PrismaRemediate-latest.zip"
cross_account_role_name = "CrossAccountRemediationRole"
```

Create an execution plan.
```
terraform plan -var-file="prisma.tfvars"
```

**Build The Infrastructure**

Apply your changes and build the Prisma AWS remediation environment.
```
terraform apply -var-file="prisma.tfvars"
```

[Terraform Language Documentation](https://www.terraform.io/docs/configuration/index.html)

