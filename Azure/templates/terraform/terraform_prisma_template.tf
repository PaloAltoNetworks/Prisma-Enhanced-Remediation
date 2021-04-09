provider "azurerm" {
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-storage-rg"
    storage_account_name = "prismatfstate"
    container_name       = "tfstate"
    key                  = "prisma.terraform.tfstate"
  }
}

resource "azurerm_resource_group" "terraform-resource-group" {
  location = var.location
  name     = "terraform-resource-group"
}

resource "azurerm_storage_account" "terraform-app-storage" {
  name                     = "terraformappstorage"
  account_replication_type = "LRS"
  account_tier             = "Standard"
  location                 = azurerm_resource_group.terraform-resource-group.location
  resource_group_name      = azurerm_resource_group.terraform-resource-group.name

  depends_on = [azurerm_resource_group.terraform-resource-group]
}

resource "azurerm_servicebus_namespace" "terraform-namespace" {
  location            = azurerm_resource_group.terraform-resource-group.location
  resource_group_name = azurerm_resource_group.terraform-resource-group.name
  name                = "terraform-namespace"
  sku                 = "standard"

  depends_on = [azurerm_resource_group.terraform-resource-group]
}

resource "azurerm_servicebus_queue" "terraform-queue" {
  name                = "terraform-queue"
  max_delivery_count  = 100
  requires_session    = true
  namespace_name      = azurerm_servicebus_namespace.terraform-namespace.name
  resource_group_name = azurerm_resource_group.terraform-resource-group.name

  depends_on = [azurerm_servicebus_namespace.terraform-namespace]
}

resource "azurerm_role_assignment" "data-sender" {
  principal_id         = azurerm_servicebus_queue.terraform-queue.id
  scope                = var.subscription_id
  role_definition_name = "Azure Service Bus Data Sender"

  depends_on = [azurerm_servicebus_queue.terraform-queue]
}

resource "azurerm_app_service_plan" "terrsform-service-plan" {
  name                = "terraform-function-service-plan"
  kind                = "FunctionApp"
  location            = azurerm_resource_group.terraform-resource-group.location
  resource_group_name = azurerm_resource_group.terraform-resource-group.name
  sku {
    size = "S1"
    tier = "Standard"
  }

  depends_on = [azurerm_resource_group.terraform-resource-group]
}

resource "azurerm_function_app" "terraform-function-app" {
  name                       = "terraform-function-app"
  app_service_plan_id        = azurerm_app_service_plan.terrsform-service-plan.id
  location                   = azurerm_resource_group.terraform-resource-group.location
  resource_group_name        = azurerm_resource_group.terraform-resource-group.name
  storage_account_name       = azurerm_storage_account.terraform-app-storage.name
  storage_account_access_key = azurerm_storage_account.terraform-app-storage.primary_access_key

  depends_on = [azurerm_app_service_plan.terrsform-service-plan, azurerm_storage_account.terraform-app-storage, azurerm_servicebus_queue.terraform-queue]
}
