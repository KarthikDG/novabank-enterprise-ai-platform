# NovaBank Enterprise AI Platform
# System Design Interview Scenarios

## Purpose

This document contains real-world Azure Data Engineering, Databricks, Analytics Engineering, MLOps, and Generative AI system design scenarios.

These questions are commonly asked in:

```text
Senior Azure Data Engineer

Lead Data Engineer

Databricks Engineer

Analytics Engineer

ML Engineer

Solution Architect

AI Engineer
```

interviews.

---

# Scenario 1
# Design a Customer 360 Platform

## Problem

A bank stores customer data in:

```text
Core Banking

CRM

Loans

Credit Cards

Mobile Banking
```

Management wants a single customer view.

---

## Proposed Solution

```text
ADF
   │
   ▼
ADLS Bronze
   │
   ▼
Databricks Silver
   │
   ▼
Customer360 Gold
   │
   ▼
Power BI + AI Agents
```

---

## Key Design Decisions

Use:

```text
Incremental Loading

Customer Keys

Golden Record Logic

Customer360 Gold Table
```

---

## Trade-Offs

| Option | Pros | Cons |
|----------|----------|----------|
| Stored Procedures | Fast | Hard to Govern |
| Databricks | Scalable | Higher Cost |
| dbt | Maintainable | Additional Layer |

---

# Scenario 2
# Design Near Real-Time Fraud Detection

## Requirement

Fraud must be detected within:

```text
1 minute
```

---

## Solution

```text
Transactions

▼

Azure Event Hub

▼

Structured Streaming

▼

Databricks

▼

Fraud Scoring

▼

Fraud Dashboard
```

---

## Key Services

```text
Event Hub

Databricks Streaming

MLflow

Power BI
```

---

## Challenges

```text
High Throughput

Duplicate Events

Latency

Scaling
```

---

# Scenario 3
# Design a Lakehouse Platform

## Requirement

Process:

```text
5 TB Daily

500 Million Transactions
```

---

## Architecture

```text
Sources

▼

ADF

▼

Bronze

▼

Silver

▼

Gold
```

---

## Why Lakehouse?

```text
Scalability

Open Formats

Machine Learning

Cost Optimization
```

---

# Scenario 4
# Design Metadata-Driven Ingestion

## Problem

500 tables need ingestion.

Traditional Approach:

```text
500 Pipelines
```

Not scalable.

---

## Solution

Metadata Table:

```text
Source

Object

Watermark

Load Type
```

Pipeline:

```text
Lookup

▼

ForEach

▼

Execute
```

---

## Benefits

```text
Reusable

Scalable

Low Maintenance
```

---

# Scenario 5
# Design Enterprise Data Quality Framework

## Requirements

Validate:

```text
Null Values

Duplicates

Reference Data

Freshness
```

---

## Solution

Silver Layer:

```text
Validation Rules

Quality Logs

Quarantine Tables
```

---

## Monitoring

Store:

```text
Failed Records

DQ Scores

Validation Results
```

---

# Scenario 6
# Design MLOps Platform

## Requirement

Deploy fraud models safely.

---

## Architecture

```text
Training

▼

MLflow

▼

Registry

▼

Approval

▼

Production
```

---

## Monitoring

```text
Accuracy

Drift

Latency

Predictions
```

---

# Scenario 7
# Design Model Drift Detection

## Requirement

Detect degradation automatically.

---

## Design

```text
Production Data

▼

Feature Drift Detection

▼

Prediction Drift Detection

▼

Alert

▼

Retraining
```

---

## Metrics

```text
KS Statistic

AUC

Recall

Precision
```

---

# Scenario 8
# Design Enterprise RAG

## Requirement

Employees ask questions about policies.

---

## Architecture

```text
PDF

▼

Chunking

▼

Embeddings

▼

Vector Search

▼

GPT-4o
```

---

## Key Components

```text
Azure OpenAI

Embeddings

Vector Database

Search Layer
```

---

# Scenario 9
# Design AI Assistant for Fraud Teams

## Requirement

Investigators need faster investigations.

---

## Agent Design

```text
Fraud Case

Transactions

Customer360

Knowledge Base

▼

Fraud Agent
```

---

## Output

```text
Investigation Summary

Fraud Indicators

Recommended Actions
```

---

# Scenario 10
# Design Enterprise Security

## Objective

Protect customer data.

---

## Components

```text
Entra ID

RBAC

Private Endpoints

Key Vault

Unity Catalog
```

---

## Controls

```text
MFA

Encryption

Masking

Audit Logs
```

---

# Scenario 11
# Design CI/CD for Data Platform

## Requirement

Deploy safely to production.

---

## Architecture

```text
GitHub

▼

Pull Request

▼

Azure DevOps

▼

Terraform

▼

Deployment
```

---

## Quality Gates

```text
Code Review

Unit Testing

Security Scan

Approval
```

---

# Scenario 12
# Design Multi-Region Disaster Recovery

## Requirement

Support regional outage.

---

## Architecture

```text
Region A

Primary

▼

Geo Replication

▼

Region B

Secondary
```

---

## Services

```text
ADLS GRS

Terraform

Databricks Backup

Database Replication
```

---

# Scenario 13
# Reduce Databricks Costs

## Problem

Monthly cost is too high.

---

## Solution

```text
Autoscaling

Job Clusters

Photon

Optimize

ZORDER

Storage Lifecycle
```

---

# Scenario 14
# Improve Slow Queries

## Problem

Customer dashboard is slow.

---

## Investigation

Check:

```text
Partitioning

Joins

OPTIMIZE

Cluster Sizing
```

---

## Resolution

```text
ZORDER

Caching

Incremental Models
```

---

# Scenario 15
# Design Executive Reporting Platform

## Requirements

```text
Daily KPIs

Fraud

Risk

Customers

Revenue
```

---

## Design

```text
Gold Models

▼

Power BI Semantic Model

▼

Executive Dashboard
```

---

# Scenario 16
# Large-Scale Streaming Platform

## Requirement

100,000 events/sec

---

## Solution

```text
Event Hub

Partitions

Structured Streaming

Checkpointing
```

---

## Considerations

```text
Ordering

Scaling

Fault Tolerance
```

---

# Scenario 17
# GDPR Compliance Design

## Requirements

```text
Right To Be Forgotten

Data Protection

Auditability
```

---

## Architecture

```text
Encryption

Masking

Retention Policies

RBAC
```

---

# Scenario 18
# Customer Segmentation Platform

## Requirement

Marketing wants customer groups.

---

## Inputs

```text
Transactions

Risk

Products

Behaviour
```

---

## Output

```text
Premium

Gold

Standard
```

---

# Scenario 19
# High Availability Data Platform

## Target

```text
99.9% Availability
```

---

## Approach

```text
Monitoring

Auto Recovery

Geo Redundancy

Alerting
```

---

# Scenario 20
# Explain Your Strongest Project

## Recommended Answer

> I designed an Azure-based Enterprise AI Platform supporting Customer360, Fraud Analytics, Risk Analytics, MLOps, and Generative AI. The solution uses Azure Data Factory, Event Hub, Databricks, Delta Lake, dbt, MLflow, Azure OpenAI, Terraform, Power BI, and Azure DevOps. The platform follows a Medallion Architecture and incorporates governance, monitoring, security, and CI/CD best practices.

---

# Architect Follow-Up Questions

Prepare to answer:

```text
Why Databricks instead of Synapse?

Why dbt?

How would you scale to 100 TB?

How would you support multiple countries?

How would you redesign for real-time processing?

How would you reduce costs?

How would you improve security?

How would you handle 10 billion records?
```

---

# Final Advice

In system design interviews:

1. Clarify requirements.
2. Estimate scale.
3. Draw high-level architecture.
4. Explain data flow.
5. Discuss scalability.
6. Discuss security.
7. Discuss monitoring.
8. Discuss cost optimisation.
9. Explain trade-offs.
10. Summarise business outcomes.

This approach consistently demonstrates senior-level engineering and solution architecture thinking.
