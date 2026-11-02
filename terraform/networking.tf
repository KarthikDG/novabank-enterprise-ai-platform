#################################################
# Virtual Network
#################################################

resource "azurerm_virtual_network" "novabank_vnet" {

  name                = "vnet-novabank-dev"
  location            = azurerm_resource_group.dev.location
  resource_group_name = azurerm_resource_group.dev.name

  address_space = [
    "10.0.0.0/16"
  ]

  tags = var.tags
}

#################################################
# Databricks Public Subnet
#################################################

resource "azurerm_subnet" "databricks_public" {

  name                 = "snet-databricks-public"
  resource_group_name  = azurerm_resource_group.dev.name
  virtual_network_name = azurerm_virtual_network.novabank_vnet.name

  address_prefixes = [
    "10.0.1.0/24"
  ]

  delegation {
    name = "databricks-public-delegation"

    service_delegation {
      name = "Microsoft.Databricks/workspaces"

      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}

#################################################
# Databricks Private Subnet
#################################################

resource "azurerm_subnet" "databricks_private" {

  name                 = "snet-databricks-private"
  resource_group_name  = azurerm_resource_group.dev.name
  virtual_network_name = azurerm_virtual_network.novabank_vnet.name

  address_prefixes = [
    "10.0.2.0/24"
  ]

  delegation {
    name = "databricks-private-delegation"

    service_delegation {
      name = "Microsoft.Databricks/workspaces"

      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}

#################################################
# Data Factory Subnet
#################################################

resource "azurerm_subnet" "adf
