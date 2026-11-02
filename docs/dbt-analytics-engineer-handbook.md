# dbt Analytics Engineer Handbook
# From Beginner to Senior Analytics Engineer

Version: 1.0

---

# Overview

This handbook covers Analytics Engineering using dbt.

Target Roles:

```text
Analytics Engineer

Senior Analytics Engineer

Data Engineer

BI Engineer

Data Platform Engineer
```

---

# Table of Contents

1. Analytics Engineering Fundamentals
2. What is dbt?
3. dbt Architecture
4. Project Structure
5. Sources
6. Staging Models
7. Intermediate Models
8. Mart Models
9. Tests
10. Snapshots
11. Seeds
12. Macros
13. Incremental Models
14. Documentation
15. Lineage
16. CI/CD
17. Best Practices
18. Production Troubleshooting
19. Interview Questions
20. Architect-Level Discussions

---

# Chapter 1
# Analytics Engineering Fundamentals

## Traditional Problems

Historically:

```text
Business Logic In Dashboards

Duplicated SQL

No Documentation

No Testing
```

---

## Analytics Engineering Solution

Moves business logic into:

```text
Version Controlled SQL

Reusable Models

Automated Testing

Documentation
```

---

# Chapter 2
# What is dbt?

dbt stands for:

```text
Data Build Tool
```

Purpose:

```text
Transform Data

Test Data

Document Data

Build Lineage
```

---

## dbt Workflow

```text
Raw Data

▼

Staging

▼

Intermediate

▼

Marts

▼

Power BI
```

---

# Chapter 3
# dbt Architecture

## Source Layer

External tables.

Example:

```sql
{{ source('customer','customer_silver') }}
```

---

## Staging Layer

Responsibilities:

```text
Rename Columns

Data Type Conversion

Standardisation
```

---

## Intermediate Layer

Responsibilities:

```text
Business Rules

Reusable Logic

Aggregations
```

---

## Mart Layer

Responsibilities:

```text
Facts

Dimensions

KPIs
```

---

# Chapter 4
# Project Structure

```text
dbt/

├── models
│
├── snapshots
│
├── tests
│
├── macros
│
├── seeds
│
└── dbt_project.yml
```

---

# Chapter 5
# Sources

## Why Sources?

Sources represent upstream systems.

Example:

```sql
{{ source(
    'customer',
    'customer_silver'
) }}
```

---

## Benefits

```text
Lineage

Documentation

Testing
```

---

# Chapter 6
# Staging Models

## Purpose

Clean source data.

Example:

```sql
select

    customer_id,

    upper(country_code)
        as country_code

from source_table
```

---

## Naming Convention

```text
stg_customer

stg_transaction
```

---

# Chapter 7
# Intermediate Models

## Purpose

Reusable logic.

Example:

```text
Customer Activity

Fraud Signals

Risk Metrics
```

---

## Naming

```text
int_customer_activity

int_fraud_signals
```

---

# Chapter 8
# Mart Models

## Purpose

Business consumption.

---

## Dimensions

```text
dim_customer

dim_account
```

---

## Facts

```text
fact_transactions

fact_fraud_cases

fact_risk_scores
```

---

# Chapter 9
# Tests

## Why Tests?

Data quality protection.

---

## Common Tests

### Unique

```yaml
tests:
  - unique
```

---

### Not Null

```yaml
tests:
  - not_null
```

---

### Accepted Values

```yaml
tests:
  - accepted_values
```

---

### Relationships

```yaml
tests:
  - relationships
```

---

# Chapter 10
# Snapshots

## Purpose

Track historical changes.

---

## Example

Customer Risk Rating

Before:

```text
LOW
```

After:

```text
HIGH
```

Snapshot stores history.

---

# Chapter 11
# Seeds

## Purpose

Small static datasets.

Examples:

```text
Countries

Exchange Rates

Reference Data
```

---

## Load

```bash
dbt seed
```

---

# Chapter 12
# Macros

## Purpose

Reusable logic.

---

## Example

```sql
{% macro current_timestamp() %}

current_timestamp

{% endmacro %}
```

---

## Benefits

```text
Reusable

Consistent

Maintainable
```

---

# Chapter 13
# Incremental Models

## Problem

Large fact tables.

---

## Solution

Load only new records.

Example:

```sql
{{ config(
    materialized='incremental'
) }}
```

---

## Benefits

```text
Faster Runs

Lower Costs

Scalable
```

---

# Chapter 14
# Documentation

Generate:

```bash
dbt docs generate
```

---

Serve:

```bash
dbt docs serve
```

---

Produces:

```text
Model Docs

Lineage

Column Metadata
```

---

# Chapter 15
# Lineage

Example:

```text
source_customer

    ▼

stg_customer

    ▼

int_customer_activity

    ▼

dim_customer
```

---

# Chapter 16
# CI/CD

Typical Pipeline

```text
dbt deps

▼

dbt compile

▼

dbt test

▼

dbt run

▼

dbt docs generate
```

---

## Quality Gate

```text
No Test Failures
```

---

# Chapter 17
# Best Practices

## Use Layers

```text
Source

Staging

Intermediate

Mart
```

---

## Keep Models Small

One responsibility per model.

---

## Document Everything

Add:

```yaml
description:
```

everywhere.

---

## Add Tests

Every model should contain:

```text
Unique

Not Null
```

where applicable.

---

# Chapter 18
# Production Troubleshooting

## Problem

dbt Run Failed.

---

### Investigation

```bash
dbt build
```

Review logs.

---

## Problem

Relationship Test Failed.

### Investigation

Check:

```text
Missing Foreign Keys

Bad Data Loads
```

---

## Problem

Duplicate Records.

### Check

```text
Source System

Joins

Incremental Logic
```

---

# Chapter 19
# Interview Questions

## Q1. What is dbt?

### Answer

Analytics engineering framework used for:

```text
Transformation

Testing

Documentation

Lineage
```

---

## Q2. What is ref()?

### Answer

References another dbt model.

Example:

```sql
{{ ref('dim_customer') }}
```

---

## Q3. What is source()?

### Answer

References upstream tables.

Example:

```sql
{{ source('customer',
           'customer_silver') }}
```

---

## Q4. Difference between table and view?

### Answer

View:

```text
Calculated Every Query
```

Table:

```text
Persisted
```

---

## Q5. Difference between incremental and full load?

### Answer

Incremental:

```text
Only New Data
```

Full:

```text
Entire Dataset
```

---

## Q6. Why use snapshots?

### Answer

Track historical changes.

---

## Q7. What are dbt tests?

### Answer

```text
Unique

Not Null

Relationships

Accepted Values
```

---

## Q8. What is lineage?

### Answer

Shows dependencies between models.

---

## Q9. Why separate staging and marts?

### Answer

Improves:

```text
Maintainability

Reusability

Testing
```

---

## Q10. How do you optimize dbt?

### Answer

```text
Incremental Models

Materializations

Efficient SQL

Partitioning
```

---

# Chapter 20
# Architecture Questions

## Why use dbt with Databricks?

### Answer

Databricks:

```text
Engineering Transformations

Streaming

Feature Engineering
```

dbt:

```text
Business Logic

Testing

Documentation

Lineage
```

---

## Why not put logic directly in Power BI?

### Answer

Problems:

```text
Duplicated Logic

No Governance

No Testing
```

dbt centralizes business logic.

---

## Senior-Level Answer

> dbt acts as the analytics engineering layer between Databricks and Power BI. It standardizes business logic, provides automated testing, creates lineage documentation, and produces reusable dimensional models that can be consumed consistently by reporting, machine learning, and AI workloads.
