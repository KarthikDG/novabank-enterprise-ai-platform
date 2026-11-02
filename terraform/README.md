# Terraform Infrastructure

## Overview

This folder contains all Infrastructure as Code (IaC) required to deploy the NovaBank Enterprise AI Platform on Microsoft Azure.

Terraform is used to provision:

- Resource Groups
- Azure Data Lake Storage Gen2
- Azure Databricks
- Azure Data Factory
- Event Hub
- Key Vault
- Azure Monitor
- Log Analytics
- Managed Identities
- Networking Components
- Security Policies

---

# Infrastructure Architecture

```text
Azure Subscription

│
├── Resource Groups
│
├── Networking
│   ├── VNet
│   ├── Subnets
│   ├── NSGs
│   └── Private Endpoints
│
├── Storage
│   └── Data Lake Gen2
│
├── Compute
│   └── Databricks Workspace
│
├── Data Integration
│   └── Azure Data Factory
│
├── Streaming
│   └── Event Hub
│
├── Security
│   ├── Key Vault
│   ├── Managed Identities
│   └── RBAC
│
└── Monitoring
    ├── Log Analytics
    └── Azure Monitor
```

---

# Environment Strategy

The platform supports multiple environments.

```text
DEV
TEST
UAT
PROD
```

Each environment has:

- Dedicated Resource Group
- Dedicated Storage
- Dedicated Databricks Workspace
- Dedicated Monitoring

---

# Resource Naming Convention

## Resource Groups

```text
rg-novabank-dev
rg-novabank-test
rg-novabank-uat
rg-novabank-prod
```

## Storage Accounts

```text
stnovabankdev
stnovabanktest
stnovabankuat
stnovabankprod
```

## Databricks

```text
adb-novabank-dev
adb-novabank-test
adb-novabank-uat
adb-novabank-prod
```

## Data Factory

```text
adf-novabank-dev
adf-novabank-test
adf-novabank-uat
adf-novabank-prod
```

---

# Deployment Order

Deploy resources in the following sequence:

## Step 1

Resource Groups

## Step 2

Networking

## Step 3

Key Vault

## Step 4

Storage Account

## Step 5

Managed Identity

## Step 6

Databricks Workspace

## Step 7

Data Factory

## Step 8

Event Hub

## Step 9

Monitoring Solutions

## Step 10

Role Assignments

---

# State Management

Terraform State should be stored remotely.

Recommended:

```text
Azure Storage Account
```

State File:

```text
terraform.tfstate
```

State Locking:

```text
Blob Lease Locking
```

---

# Security Principles

Implemented controls include:

- Least Privilege Access
- RBAC
- Encryption at Rest
- Encryption in Transit
- Managed Identity
- Private Networking
- Secret Management via Key Vault

---

# Modules

```text
modules/

├── resource-group
├── storage-account
├── databricks
├── data-factory
├── eventhub
├── keyvault
├── monitor
├── networking
└── security
```

---

# Environments

```text
environments/

├── dev
├── test
├── uat
└── prod
```

---

# Deployment

Initialize Terraform:

```bash
terraform init
```

Validate Configuration:

```bash
terraform validate
```

Create Execution Plan:

```bash
terraform plan
```

Deploy Resources:

```bash
terraform apply
```

---

# Next Files

The next Terraform files to be created are:

```text
providers.tf
backend.tf
main.tf
variables.tf
resource-groups.tf
networking.tf
storage.tf
keyvault.tf
databricks.tf
adf.tf
eventhub.tf
monitoring.tf
outputs.tf
```
