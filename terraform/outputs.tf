#################################################
# Resource Group
#################################################

output "resource_group_name" {

  description = "Resource Group Name"

  value = azurerm_resource_group.dev.name
}

#################################################
# Storage Account
#################################################

output "storage_account_name" {

  description = "Azure Data Lake Storage Account"

  value = azurerm_storage_account.datalake.name
}

output "storage_account_id" {

  description = "Azure Data Lake Storage Account ID"

  value = azurerm_storage_account.datalake.id
}

#################################################
# Data Lake Containers
#################################################

output "bronze_container_name" {

  value = azurerm_storage_container.bronze.name
}

output "silver_container_name" {

  value = azurerm_storage_container.silver.name
}

output "gold_container_name" {

  value = azurerm_storage_container.gold.name
}

#################################################
# Key Vault
#################################################

output "key_vault_name" {

  description = "Azure Key Vault Name"

  value = azurerm_key_vault.novabank_kv.name
}

output "key_vault_uri" {

  description = "Azure Key Vault URI"

  value = azurerm_key_vault.novabank_kv.vault_uri
}

#################################################
# Databricks
#################################################

output "databricks_workspace_name" {

  description = "Databricks Workspace"

  value = azurerm_databricks_workspace.novabank_databricks.name
}

output "databricks_workspace_url" {

  description = "Databricks Workspace URL"

  value = azurerm_databricks_workspace.novabank_databricks.workspace_url
}

#################################################
# Azure Data Factory
#################################################

output "data_factory_name" {

  description = "Azure Data Factory"

  value = azurerm_data_factory.novabank_adf.name
}

#################################################
# Event Hub
#################################################

output "eventhub_namespace_name" {

  description = "Event Hub Namespace"

  value = azurerm_eventhub_namespace.novabank.name
}

output "payment_eventhub_name" {

  value = azurerm_eventhub.payment_transactions.name
}

output "fraud_eventhub_name" {

  value = azurerm_eventhub.fraud_alerts.name
}

#################################################
# Monitoring
#################################################

output "log_analytics_workspace_name" {

  description = "Log Analytics Workspace"

  value = azurerm_log_analytics_workspace.novabank_logs.name
}

output "application_insights_name" {

  description = "Application Insights"

  value = azurerm_application_insights.novabank_insights.name
}

#################################################
# Networking
#################################################

output "virtual_network_name" {

  value = azurerm_virtual_network.novabank_vnet.name
}

output "databricks_public_subnet" {

  value = azurerm_subnet.databricks_public.name
}

output "databricks_private_subnet" {

  value = azurerm_subnet.databricks_private.name
}

#################################################
# Environment
#################################################

output "environment" {

  value = var.environment
}

output "deployment_location" {

  value = var.location
}
