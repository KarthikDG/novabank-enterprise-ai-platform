#################################################
# Resource Group
#################################################

module "resource_group" {

  source = "./modules/resource-group"

  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags
}

#################################################
# Data Lake Storage
#################################################

module "storage" {

  source = "./modules/storage-account"

  resource_group_name = module.resource_group.resource_group_name
  location            = var.location
  storage_account_name = var.storage_account_name

  containers = var.containers

  tags = var.tags
}

#################################################
# Azure Key Vault
#################################################

module "keyvault" {

  source = "./modules/keyvault"

  resource_group_name = module.resource_group.resource_group_name
  location            = var.location

  key_vault_name = var.key_vault_name

  tags = var.tags
}

#################################################
# Azure Databricks
#################################################

module "databricks" {

  source = "./modules/databricks"

  resource_group_name = module.resource_group.resource_group_name
  location            = var.location

  databricks_workspace_name = var.databricks_workspace_name

  tags = var.tags
}

#################################################
# Azure Data Factory
#################################################

module "data_factory" {

  source = "./modules/data-factory"

  resource_group_name = module.resource_group.resource_group_name
  location            = var.location

  data_factory_name = var.data_factory_name

  tags = var.tags
}

#################################################
# Event Hub
#################################################

module "eventhub" {

  source = "./modules/eventhub"

  resource_group_name = module.resource_group.resource_group_name
  location            = var.location

  eventhub_namespace_name = var.eventhub_namespace_name

  tags = var.tags
}

#################################################
# Monitoring
#################################################

module "monitoring" {

  source = "./modules/monitor"

  resource_group_name = module.resource_group.resource_group_name
  location            = var.location

  log_analytics_workspace_name =
    var.log_analytics_workspace_name

  tags = var.tags
}
