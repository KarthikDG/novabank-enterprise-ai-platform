#################################################
# Current Azure Client Configuration
#################################################

data "azurerm_client_config" "current" {}

#################################################
# Azure Key Vault
#################################################

resource "azurerm_key_vault" "novabank_kv" {

  name                        = var.key_vault_name
  location                    = azurerm_resource_group.dev.location
  resource_group_name         = azurerm_resource_group.dev.name

  tenant_id                   = data.azurerm_client_config.current.tenant_id

  sku_name                    = "standard"

  soft_delete_retention_days  = 90

  purge_protection_enabled    = true

  enabled_for_disk_encryption = true

  public_network_access_enabled = false

  tags = var.tags
}

#################################################
# Key Vault Administrator Access Policy
#################################################

resource "azurerm_key_vault_access_policy" "current_user" {

  key_vault_id = azurerm_key_vault.novabank_kv.id

  tenant_id = data.azurerm_client_config.current.tenant_id
  object_id = data.azurerm_client_config.current.object_id

  secret_permissions = [
    "Get",
    "List",
    "Set",
    "Delete",
    "Recover",
    "Backup",
    "Restore",
    "Purge"
  ]

  key_permissions = [
    "Get",
    "List",
    "Create",
    "Delete",
    "Update"
  ]
}

#################################################
# Databricks PAT Secret
#################################################

resource "azurerm_key_vault_secret" "databricks_pat" {

  name
