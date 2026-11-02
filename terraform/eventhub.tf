#################################################
# Event Hub Namespace
#################################################

resource "azurerm_eventhub_namespace" "novabank" {

  name                = var.eventhub_namespace_name

  location            = azurerm_resource_group.dev.location
  resource_group_name = azurerm_resource_group.dev.name

  sku      = "Standard"
  capacity = 2

  auto_inflate_enabled     = true
  maximum_throughput_units = 10

  local_authentication_enabled = true

  tags = var.tags
}

#################################################
# Payment Transactions Event Hub
#################################################

resource "azurerm_eventhub" "payment_transactions" {

  name                = "payment-transactions"

  namespace_name      = azurerm_eventhub_namespace.novabank.name
  resource_group_name = azurerm_resource_group.dev.name

  partition_count   = 8
  message_retention = 7
}

#################################################
# Fraud Alerts Event Hub
#################################################

resource "azurerm_eventhub" "fraud_alerts" {

  name                = "fraud-alerts"

  namespace_name      = azurerm_eventhub_namespace.novabank.name
  resource_group_name = azurerm_resource_group.dev.name

  partition_count   = 4
  message_retention = 7
}

#################################################
# Customer Activity Event Hub
#################################################

resource "azurerm_eventhub" "customer_activity" {

  name                = "customer-activity"

  namespace_name      = azurerm_eventhub_namespace.novabank.name
  resource_group_name = azurerm_resource_group.dev.name

  partition_count   = 8
  message_retention = 7
}

#################################################
# Mobile Banking Event Hub
#################################################

resource "azurerm_eventhub" "mobile_banking" {

  name                = "mobile-banking"

  namespace_name      = azurerm_eventhub_namespace.novabank.name
  resource_group_name = azurerm_resource_group.dev.name

  partition_count   = 8
  message_retention = 7
}

#################################################
# ATM Transactions Event Hub
#################################################

resource "azurerm_eventhub" "atm_transactions" {

  name                = "atm-transactions"

  namespace_name      = azurerm_eventhub_namespace.novabank.name
  resource_group_name = azurerm_resource_group.dev.name

  partition_count   = 4
  message_retention = 7
}

#################################################
# Shared Access Policy
#################################################

resource "azurerm_eventhub_namespace_authorization_rule" "streaming_access" {

  name                = "streaming-access"

  namespace_name      = azurerm_eventhub_namespace.novabank.name
  resource_group_name = azurerm_resource_group.dev.name

  listen = true
  send   = true
  manage = true
}
