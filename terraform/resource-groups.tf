#################################################
# Resource Groups
#################################################

resource "azurerm_resource_group" "dev" {

  name     = "rg-novabank-dev"
  location = var.location

  tags = merge(
    var.tags,
    {
      environment = "dev"
    }
  )
}

resource "azurerm_resource_group" "test" {

  name     = "rg-novabank-test"
  location = var.location

  tags = merge(
    var.tags,
    {
      environment = "test"
    }
  )
}

resource "azurerm_resource_group" "uat" {

  name     = "rg-novabank-uat"
  location = var.location

  tags = merge(
    var.tags,
    {
      environment = "uat"
    }
  )
}

resource "azurerm_resource_group" "prod" {

  name     = "rg-novabank-prod"
  location = var.location

  tags = merge(
    var.tags,
    {
      environment = "prod"
    }
  )
}
