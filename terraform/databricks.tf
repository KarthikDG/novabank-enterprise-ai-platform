#################################################
# Managed Identity
#################################################

resource "azurerm_user_assigned_identity" "databricks_identity" {

  name                = "id-novabank-databricks"
  location            = azurerm_resource_group.dev.location
  resource_group_name = azurerm_resource_group.dev.name

  tags = var.tags
}

#################################################
# Azure Databricks Workspace
#################################################

resource "azurerm_databricks_workspace" "novabank_databricks" {

  name                = var.databricks_workspace_name

  location            = azurerm_resource_group.dev.location
  resource_group_name = azurerm_resource_group.dev.name

  sku = "premium"

  managed_resource_group_name =
    "rg-managed-novabank-databricks"

  public_network_access_enabled = false

  customer_managed_key_enabled = false

  infrastructure_encryption_enabled = true

  tags = var.tags
}

#################################################
# Databricks Access Connector
##########################################
