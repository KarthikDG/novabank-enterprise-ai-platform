#################################################
# Azure Data Lake Storage Gen2
#################################################

resource "azurerm_storage_account" "datalake" {

  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.dev.name
  location                 = azurerm_resource_group.dev.location

  account_tier             = "Standard"
  account_replication_type = "LRS"

  account_kind = "StorageV2"

  is_hns_enabled = true

  min_tls_version = "TLS1_2"

  allow_nested_items_to_be_public = false

  tags = var.tags
}

#################################################
# Bronze Container
#################################################

resource "azurerm_storage_container" "bronze" {

  name                  = "bronze"
  storage_account_id    = azurerm_storage_account.datalake.id
  container_access_type = "private"
}

#################################################
# Silver Container
#################################################

resource "azurerm_storage_container" "silver" {

  name                  = "silver"
  storage_account_id    = azurerm_storage_account.datalake.id
  
