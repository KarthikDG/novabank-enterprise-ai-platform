################################################
# Global Variables
################################################

variable "project_name" {
  description = "Project Name"
  type        = string
  default     = "novabank"
}

variable "environment" {
  description = "Deployment Environment"
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure Region"
  type        = string
  default     = "westeurope"
}

################################################
# Resource Group
################################################

variable "resource_group_name" {
  description = "Resource Group Name"
  type        = string
  default     = "rg-novabank-dev"
}

################################################
# Storage Account
################################################

variable "storage_account_name" {
  description = "ADLS Storage Account"
  type        = string
}

################################################
# Data Lake Containers
################################################

variable "containers" {

  type = list(string)

  default = [
    "bronze",
    "silver",
    "gold",
    "archive",
    "quarantine"
  ]
}

################################################
# Databricks
################################################

variable "databricks_workspace_name" {
  description = "Databricks Workspace Name"
  type        = string
}

variable "databricks_workspace_url" {
  description = "Databricks Workspace URL"
  type        = string
  default     = ""
}

################################################
# Azure Data Factory
################################################

variable "data_factory_name" {
  description = "Azure Data Factory Name"
  type        = string
}

################################################
# Event Hub
################################################

variable "eventhub_namespace_name" {
  description = "Event Hub Namespace"
  type        = string
}

################################################
# Key Vault
################################################

variable "key_vault_name" {
  description = "Azure Key Vault Name"
  type        = string
}

################################################
# Logging
################################################

variable "log_analytics_workspace_name" {
  description = "Log Analytics Workspace"
  type        = string
}

################################################
# Tags
################################################

variable "tags" {

  description = "Common Tags"

  type = map(string)

  default = {
    project     = "NovaBank"
    owner       = "DataEngineering"
    environment = "dev"
    managed_by  = "Terraform"
  }
}
