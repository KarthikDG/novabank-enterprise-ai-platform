#################################################
# Log Analytics Workspace
#################################################

resource "azurerm_log_analytics_workspace" "novabank_logs" {

  name                = var.log_analytics_workspace_name
  location            = azurerm_resource_group.dev.location
  resource_group_name = azurerm_resource_group.dev.name

  sku               = "PerGB2018"
  retention_in_days = 30

  tags = var.tags
}

#################################################
# Application Insights
#################################################

resource "azurerm_application_insights" "novabank_insights" {

  name                = "appi-novabank-dev"
  location            = azurerm_resource_group.dev.location
  resource_group_name = azurerm_resource_group.dev.name

  workspace_id = azurerm_log_analytics_workspace.novabank_logs.id

  application_type = "web"

  tags = var.tags
}

#################################################
# Azure Monitor Action Group
#################################################

resource "azurerm_monitor_action_group" "novabank_ops" {

  name                = "ag-novabank-ops"
  resource_group_name = azurerm_resource_group.dev.name

  short_name = "NBOPS"

  email_receiver {

    name                    = "OperationsTeam"
    email_address           = "operations@novabank.internal"
    use_common_alert_schema = true
  }

  tags = var.tags
}

#################################################
# Storage Capacity Alert
#################################################

resource "azurerm_monitor_metric_alert" "storage_capacity_alert" {

  name                = "alert-storage-capacity"
  resource_group_name = azurerm_resource_group.dev.name

  scopes = [
    azurerm_storage_account.datalake.id
  ]

  description = "Storage account capacity threshold exceeded."

  severity = 2

  frequency   = "PT5M"
  window_size = "PT15M"

  criteria {

    metric_namespace = "Microsoft.Storage/storageAccounts"

    metric_name = "UsedCapacity"

    aggregation = "Average"

    operator = "GreaterThan"

    threshold = 100000000000
  }

  action {
    action_group_id =
      azurerm_monitor_action_group.novabank_ops.id
  }

  tags = var.tags
}

#################################################
# Event Hub Throughput Alert
#################################################

resource "azurerm_monitor_metric_alert" "eventhub_alert" {

  name                = "alert-eventhub-throughput"
  resource_group_name = azurerm_resource_group.dev.name

  scopes = [
    azurerm_eventhub_namespace.novabank.id
  ]

  description = "Event Hub throughput threshold exceeded."

  severity = 2

  frequency   = "PT5M"
  window_size = "PT15M"

  criteria {

    metric_namespace =
      "Microsoft.EventHub/namespaces"

    metric_name = "IncomingMessages"

    aggregation = "Total"

    operator = "GreaterThan"

    threshold = 100000
  }

  action {
    action_group_id =
      azurerm_monitor_action_group.novabank_ops.id
  }

  tags = var.tags
}

#################################################
# Databricks Diagnostics
#################################################

resource "azurerm_monitor_diagnostic_setting" "databricks_diag" {

  name = "diag-databricks"

  target_resource_id =
    azurerm_databricks_workspace.novabank_databricks.id

  log_analytics_workspace_id =
    azurerm_log_analytics_workspace.novabank_logs.id

  enabled_log {
    category = "dbfs"
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
