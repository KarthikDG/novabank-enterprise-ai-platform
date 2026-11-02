terraform {
  required_version = ">= 1.7.0"

  required_providers {

    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }

    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 3.0"
    }

    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.50"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }

  }
}

provider "azurerm" {
  features {}
}

provider "azuread" {
}

provider "databricks" {
  host = var.databricks_workspace_url
}

provider "random" {
}
