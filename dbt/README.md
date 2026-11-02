# dbt Analytics Engineering Layer

## Overview

dbt (Data Build Tool) is responsible for transforming curated Silver layer data into trusted business-ready Gold models.

The Analytics Engineering layer provides:

- Business Transformations
- Data Modelling
- Data Quality Testing
- Documentation
- Lineage
- Dimensional Modelling
- KPI Standardisation

---

# Architecture

```text
Bronze Layer
      │
      ▼

Silver Layer
      │
      ▼

dbt Transformations
      │
      ▼

Gold Layer
      │
      ├── Power BI
      ├── Data Science
      ├── Fraud Analytics
      ├── Risk Analytics
      └── GenAI
```

---

# Project Structure

```text
dbt/

├── README.md

├── models/
│   ├── staging/
│   ├── intermediate/
│   ├── marts/
│   └── metrics/
│
├── tests/
│
├── snapshots/
│
├── macros/
│
├── seeds/
│
└── analyses/
```

---

# Layer Design

## Staging Layer

Purpose:

```text
Light Transformations
Column Renaming
Type Casting
Source Standardisation
```

Examples:

```text
stg_customer

stg_transaction

stg_loan

stg_mortgage
```

---

## Intermediate Layer

Purpose:

```text
Reusable Business Logic
Complex Transformations
Business Rules
```

Examples:

```text
int_customer_activity

int_fraud_signals

int_risk_exposure
```

---

## Mart Layer

Purpose:

```text
Business Consumption
Reporting
Analytics
Machine Learning
```

Examples:

```text
dim_customer

fact_transactions

fact_fraud_cases

fact_risk_scores
```

---

# Business Domains

## Customer Domain

Tables:

```text
stg_customer

int_customer_activity

dim_customer
```

---

## Transaction Domain

Tables:

```text
stg_transaction

int_transaction_metrics

fact_transactions
```

---

## Fraud Domain

Tables:

```text
int_fraud_signals

fact_fraud_cases
```

---

## Risk Domain

Tables:

```text
int_risk_metrics

fact_risk_scores
```

---

# Naming Convention

## Staging

```text
stg_<domain>
```

Examples:

```text
stg_customer

stg_transaction
```

---

## Intermediate

```text
int_<domain>_<purpose>
```

Examples:

```text
int_customer_activity

int_fraud_signals
```

---

## Facts

```text
fact_<subject>
```

Examples:

```text
fact_transactions

fact_fraud_cases
```

---

## Dimensions

```text
dim_<subject>
```

Examples:

```text
dim_customer

dim_account
```

---

# Testing Strategy

dbt tests validate:

```text
Uniqueness

Not Null

Referential Integrity

Accepted Values

Data Consistency
```

Example:

```yaml
tests:
  - unique
  - not_null
```

---

# Snapshots

Snapshots track historical changes.

Examples:

```text
Customer Risk Rating

KYC Status

Fraud Risk Category
```

Snapshot Benefits:

```text
Historical Analysis

Auditability

Regulatory Compliance
```

---

# Documentation

dbt automatically generates:

```text
Lineage Graphs

Model Documentation

Column Documentation

Dependency Mapping
```

Generate Docs:

```bash
dbt docs generate
```

Serve Docs:

```bash
dbt docs serve
```

---

# CI/CD

Deployment Pipeline:

```text
Developer
    │
    ▼

Pull Request
    │
    ▼

dbt Test
    │
    ▼

dbt Run
    │
    ▼

Deployment
```

---

# Power BI Integration

Power BI consumes:

```text
dim_customer

fact_transactions

fact_fraud_cases

fact_risk_scores

customer360_gold
```

---

# dbt Benefits

```text
Version Controlled

Reusable SQL

Automated Testing

Automated Documentation

Enterprise Lineage

Analytics Governance
```

---

# Future Models

```text
models/

staging/

├── stg_customer.sql
├── stg_transaction.sql
├── stg_loan.sql

intermediate/

├── int_customer_activity.sql
├── int_fraud_signals.sql

marts/

├── dim_customer.sql
├── fact_transactions.sql
├── fact_fraud_cases.sql
└── fact_risk_scores.sql
```

---

# Next Deliverables

The next files to be created are:

```text
dbt_project.yml

models/staging/stg_customer.sql

models/staging/stg_transaction.sql

models/marts/dim_customer.sql

models/marts/fact_transactions.sql
```

These models form the analytics layer consumed by reporting, fraud analytics, machine learning, and GenAI applications.
