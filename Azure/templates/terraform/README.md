## Using Terraform

**Authentication**

Azure [Authentication](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs#authenticating-to-azure)

Recommended:

**Configuration**

```
az login
az account list

az account set --subscription="SUBSCRIPTION_ID"
```

```
# We strongly recommend using the required_providers block to set the
# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.46.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}
```

Initialize your working directory containing the Terraform configuration files.
```
terraform init -backend-config="prisma.config"
```

Update your variables as needed.

```
location        = "East US"
subscription_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
tenant_id       = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

Create an execution plan.
```
terraform plan -var-file="prisma.tfvars"
```

**Infrastructure**

Apply your changes and build the Prisma Azure remediation environment.
```
terraform apply -var-file="prisma.tfvars"
```


[Terraform Language Documentation](https://www.terraform.io/docs/configuration/index.html)

