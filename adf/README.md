# Azure Data Factory Framework

## Overview

Azure Data Factory (ADF) is responsible for ingesting data from various source systems into the NovaBank Enterprise AI Platform.

The framework supports:

- Batch Ingestion
- Incremental Loading
- CDC Processing
- Metadata-Driven Pipelines
- Error Handling
- Monitoring
- Retry Framework
- Parallel Processing

---

# Business Objectives

The ingestion platform must support:

- Core Banking Systems
- Payment Systems
- CRM Systems
- Mobile Banking Applications
- ATM Networks
- AML Systems
- Regulatory Data Sources

Expected volume:

```text
500+ Million Transactions Daily
5+ TB Data Daily
```

---

# ADF Architecture

```text
Source Systems

   |
   v

Azure Data Factory

   |
   +------------------+
   | Metadata Driven  |
   | Framework        |
   +------------------+

   |
   v

Azure Data Lake

Bronze Layer

   |
   v

Databricks Processing
```

---

# Folder Structure

```text
adf/

├── README.md

├── pipelines/
│
├── datasets/
│
├── linked-services/
│
├── triggers/
│
└── metadata-framework/
```

---

# Source Systems

## Core Banking

```text
Customers
Accounts
Loans
Mortgages
Deposits
```

## Payment Systems

```text
SEPA
Card Transactions
ATM Transactions
POS Transactions
```

## CRM

```text
Customer Interactions
Marketing Data
Customer Profiles
```

## Regulatory Sources

```text
KYC Data
AML Data
Sanction Lists
```

---

# Ingestion Patterns

## Full Load

Used for:

```text
Reference Data
Lookup Tables
Dimension Tables
```

---

## Incremental Load

Used for:

```text
Customer Transactions
Account Updates
CRM Updates
```

Example:

```sql
SELECT *
FROM Transactions
WHERE LastModifiedDate > WatermarkDate
```

---

## CDC

Used for:

```text
Insert
Update
Delete
```

Tracking.

---

# Pipeline Categories

## Customer Pipeline

```text
PL_Customer_Ingestion
```

Loads:

```text
Customer
Customer Address
Customer Contact
```

---

## Transaction Pipeline

```text
PL_Transaction_Ingestion
```

Loads:

```text
Payments
ATM
Cards
Transfers
```

---

## Loan Pipeline

```text
PL_Loan_Ingestion
```

Loads:

```text
Mortgage
Personal Loans
Business Loans
```

---

# Metadata Framework

The ingestion framework is metadata driven.

Control table contains:

```text
Source Name
Source Type
Load Type
Watermark Column
Target Path
Active Flag
```

Benefits:

- Minimal Code Changes
- Scalable
- Reusable
- Low Maintenance

---

# Error Handling

Failed records are redirected to:

```text
quarantine
```

container.

Stored information:

```text
Pipeline Name
Error Message
Timestamp
Record Count
```

---

# Monitoring

ADF Monitoring captures:

```text
Pipeline Runs
Activity Runs
Trigger Runs
Duration
Failures
```

---

# Retry Strategy

Retry Count:

```text
3
```

Retry Interval:

```text
5 Minutes
```

---

# Security

Implemented:

```text
Managed Identity
RBAC
Private Networking
Key Vault Integration
```

---

# Deployment

Deployment is automated using:

```text
Azure DevOps
Terraform
GitHub Integration
```

---

# Naming Standards

Pipelines:

```text
PL_<Domain>_<Operation>
```

Examples:

```text
PL_Customer_Ingestion
PL_Transaction_Ingestion
PL_Loan_Ingestion
```

Datasets:

```text
DS_<Source>_<Object>
```

Examples:

```text
DS_CRM_Customers
DS_CoreBanking_Accounts
```

Triggers:

```text
TR_<Domain>_<Frequency>
```

Examples:

```text
TR_Customer_Daily
TR_Transaction_15Min
```

---

# Next Deliverables

The next components to be created are:

```text
adf/pipelines/

PL_Customer_Ingestion.json

PL_Transaction_Ingestion.json

PL_Metadata_Driver.json
```

These pipelines form the core ingestion layer of the platform.
