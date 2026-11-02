terraform {

  backend "azurerm" {

    resource_group_name  = "rg-novabank-tfstate"
    storage_account_name = "stnovabanktfstate"
    container_name       = "tfstate"
    key                  = "novabank-prod.tfstate"

  }

}
