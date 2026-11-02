#################################################
# Azure Data Factory
#################################################

resource "azurerm_data_factory" "novabank_adf" {

  name                = var.data_factory_name

  location            = azurerm_resource_group.dev.location

  resource_group_name = azurerm_resource_group.dev.name

  managed_virtual_network_enabled = true

  public_network_enabled = false

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

#################################################
# GitHub Integration Variables
#################################################

resource "azurerm_data_factory_github_configuration" "github" {

  data_factory_id = azurerm_data_factory.novabank_adf.id

  account_name    = "KarthikDG"

  branch_name     = "main"

  repository_name = "novabank-enterprise-ai-platform"

  root_folder     = "/adf"
}

#################################################
# Data Factory Diagnostic Settings
#################################################

resource "azurerm_monitor_diagnostic_setting" "adf_diagnostics" {

  name = "diag-adf"

  target_resource_id =
    azurerm_data_factory.novabank_adf.id

  log_analytics_workspace_id =
    azurerm_log_analytics_workspace.novabank_logs.id

  enabled_log {
    category = "PipelineRuns"
  }

  enabled_log {
    category = "ActivityRuns"
  }

  enabled_log {
    category = "TriggerRuns"
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

#################################################
# RBAC - Storage Access
#################################################

resource "azurerm_role_assignment" "adf_storage_access" {

  scope =
    azurerm_storage_account.datalake.id

  role_definition_name =
    "Storage Blob Data Contributor"

  principal_id =
    azurerm_data_factory.novabank_adf.identity[0].principal_id
}

#################################################
# RBAC - Key Vault Access
#################################################

resource "azurerm_role_assignment" "adf_keyvault_access" {

  scope =
    azurerm_key_vault.novabank_kv.id

  role_definition_name =
    "Key Vault Secrets User"

  principal_id =
    azurerm_data_factory.novabank_adf.identity[0].principal_id
}
