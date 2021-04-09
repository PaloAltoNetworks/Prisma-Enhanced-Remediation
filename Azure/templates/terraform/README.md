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

[Terraform Language Documentation](https://www.terraform.io/docs/configuration/index.html)

