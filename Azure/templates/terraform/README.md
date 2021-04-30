## Using Terraform (Under Construction)

**Authentication**

Azure [Authentication](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs#authenticating-to-azure)

Recommended:

**Configuration**


Initialize your working directory containing Terraform configuration files.
```
terraform init -backend-config="prisma.config"
```

Update the variables as needed.


Create an execution plan.
```
terraform plan -var-file="prisma.tfvars"
```

**Infrastructure**

Apply your changes and build the Prisma AWS remediation environment.
```
terraform apply -var-file="prisma.tfvars"
```

**Testing from your local environment**

Setup:
```
export AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXXXXXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

terraform init -backend-config="prisma.config"
terraform plan -var-file="prisma.tfvars"
terraform apply -var-file="prisma.tfvars"
```

Tear down:
```
terraform destroy
```

[Terraform Language Documentation](https://www.terraform.io/docs/configuration/index.html)

