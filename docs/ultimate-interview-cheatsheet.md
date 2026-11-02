# ULTIMATE INTERVIEW CHEATSHEET
# Azure Data Engineering | Databricks | dbt | MLOps | GenAI | Solution Architecture

Version: 1.0

---

# 30-SECOND INTRODUCTION

> I designed an enterprise-scale Azure Lakehouse platform using Azure Data Factory, Azure Databricks, Delta Lake, dbt, MLflow, Azure OpenAI, Terraform, Azure DevOps, and Power BI. The platform supports Customer360, Fraud Analytics, Risk Analytics, MLOps, and Generative AI while implementing enterprise-grade security, governance, monitoring, and CI/CD.

---

# 2-MINUTE PROJECT EXPLANATION

## Business Problem

The bank had data spread across multiple systems:

```text
Core Banking

Payments

CRM

Loans

Risk Systems
```

This created:

```text
Data Silos

Slow Reporting

Manual Fraud Analysis

Limited AI Capability
```

---

## Solution

Built a modern Azure Lakehouse:

```text
ADF + Event Hub

▼

ADLS Gen2

▼

Databricks

▼

Bronze

Silver

Gold

▼

dbt

▼

Power BI

MLflow

Azure OpenAI
```

---

## Outcomes

```text
Customer360

Fraud Detection

Risk Analytics

MLOps

AI Assistants
```

---

# 5-MINUTE PROJECT EXPLANATION

## Sources

```text
Core Banking

CRM

Payments

KYC

AML
```

---

## Ingestion

```text
Azure Data Factory

Azure Event Hub
```

---

## Storage

```text
ADLS Gen2

Bronze

Silver

Gold
```

---

## Processing

```text
Databricks

PySpark

Delta Lake
```

---

## Analytics Engineering

```text
dbt

Dimensions

Facts

Lineage

Testing
```

---

## Reporting

```text
Power BI

Executive Dashboards

Fraud Dashboards

Risk Dashboards
```

---

## AI

```text
MLflow

Fraud Models

Azure OpenAI

RAG

AI Agents
```

---

# 10-MINUTE ARCHITECTURE WALKTHROUGH

## Step 1

Source systems generate data.

---

## Step 2

ADF loads batch data.

Event Hub processes streaming data.

---

## Step 3

Raw data stored in Bronze.

---

## Step 4

Databricks creates Silver datasets:

```text
Validated

Enriched

Standardized
```

---

## Step 5

dbt creates business models:

```text
dim_customer

fact_transactions

fact_fraud_cases

fact_risk_scores
```

---

## Step 6

Power BI creates dashboards.

---

## Step 7

MLflow trains fraud models.

---

## Step 8

Azure OpenAI powers AI assistants.

---

# TOP 25 ADF QUESTIONS

## Q1

What is ADF?

Answer:

Cloud-native data integration service.

---

## Q2

What is a Pipeline?

Answer:

Container for activities.

---

## Q3

What is Metadata Driven ETL?

Answer:

Load configuration stored in metadata tables.

---

## Q4

What is Lookup Activity?

Answer:

Reads configuration data.

---

## Q5

What is ForEach Activity?

Answer:

Loops through multiple items.

---

## Q6

Difference between Dataset and Linked Service?

Answer:

```text
Linked Service = Connection

Dataset = Data Object
```

---

## Q7

What is Watermark Loading?

Answer:

Incremental loading using timestamps.

---

## Q8

What is CDC?

Answer:

Change Data Capture.

---

## Q9

How do you restart failed loads?

Answer:

Checkpointing + Metadata Tracking.

---

## Q10

How do you handle 1000 tables?

Answer:

Metadata Framework.

---

# TOP 25 DATABRICKS QUESTIONS

## Q1

What is Databricks?

Unified analytics platform built on Spark.

---

## Q2

What is Spark?

Distributed processing engine.

---

## Q3

Driver vs Executor?

```text
Driver = Coordinator

Executor = Worker
```

---

## Q4

What is Delta Lake?

ACID table format.

---

## Q5

What is Time Travel?

Query old versions.

---

## Q6

What is OPTIMIZE?

Compact files.

---

## Q7

What is ZORDER?

Improve filtering performance.

---

## Q8

What is Data Skew?

Uneven data distribution.

---

## Q9

What causes Shuffle?

```text
join

groupBy

distinct
```

---

## Q10

What is Photon?

Databricks query engine.

---

# TOP 25 dbt QUESTIONS

## Q1

What is dbt?

Analytics Engineering Framework.

---

## Q2

What is ref()?

Reference another dbt model.

---

## Q3

What is source()?

Reference source tables.

---

## Q4

What are snapshots?

Historical tracking.

---

## Q5

What are incremental models?

Load only changed data.

---

## Q6

Why use dbt?

```text
Testing

Documentation

Lineage
```

---

## Q7

Why separate staging and marts?

Maintainability.

---

# TOP 25 MLOPS QUESTIONS

## Q1

What is MLOps?

Operationalizing machine learning.

---

## Q2

Why MLflow?

Tracking + Registry + Deployment.

---

## Q3

What is Feature Drift?

Features change over time.

---

## Q4

What is Prediction Drift?

Predictions shift unexpectedly.

---

## Q5

What is Model Registry?

Stores model versions.

---

## Q6

How do you rollback a model?

Deploy previous version.

---

# TOP 25 GENAI QUESTIONS

## Q1

What is RAG?

Retrieval Augmented Generation.

---

## Q2

Why use RAG?

Reduce hallucinations.

---

## Q3

What are embeddings?

Vector representations of text.

---

## Q4

What is vector search?

Similarity-based retrieval.

---

## Q5

What is chunking?

Breaking documents into sections.

---

## Q6

What causes hallucination?

Missing or poor context.

---

# STAR STORIES

## STAR STORY 1
### Customer360

#### Situation

Customer data fragmented.

#### Task

Create unified view.

#### Action

Built Customer360 platform.

#### Result

Improved visibility and customer insights.

---

## STAR STORY 2
### Fraud Detection

#### Situation

Fraud detection too slow.

#### Task

Near-real-time monitoring.

#### Action

Implemented:

```text
Event Hub

Streaming

Fraud Scoring
```

#### Result

Reduced detection latency.

---

## STAR STORY 3
### AI Assistant

#### Situation

Policy search inefficient.

#### Task

Improve knowledge discovery.

#### Action

Built Azure OpenAI RAG platform.

#### Result

Faster information retrieval.

---

# PRODUCTION SUPPORT SCENARIOS

## Databricks Job Failed

Check:

```text
Job Logs

Cluster Logs

Storage Access

Permissions
```

---

## ADF Pipeline Failed

Check:

```text
Monitor

Linked Service

Source Connectivity
```

---

## dbt Tests Failed

Check:

```text
Duplicates

Null Values

Bad Source Data
```

---

## Model Accuracy Dropped

Check:

```text
Feature Drift

Prediction Drift

Training Data
```

---

# ARCHITECT QUESTIONS

## Why Databricks Instead of Synapse?

Answer:

```text
Better Spark

Delta Lake

MLflow

Streaming
```

---

## Why Lakehouse?

Answer:

```text
Unified Analytics

Lower Cost

AI Ready
```

---

## How Would You Scale To 10 Billion Records?

Answer:

```text
Partitioning

Incremental Loads

Streaming

Photon
```

---

## How Do You Improve Performance?

Answer:

```text
Caching

Partitioning

OPTIMIZE

ZORDER

Broadcast Joins
```

---

# FINAL INTERVIEW CLOSING ANSWER

> My strongest project is the NovaBank Enterprise AI Platform. I designed a complete Azure Lakehouse solution using Azure Data Factory, Databricks, Delta Lake, dbt, MLflow, Azure OpenAI, and Power BI. The platform supports Customer360, Fraud Analytics, Risk Management, MLOps, and Generative AI use cases. It incorporates security, governance, monitoring, CI/CD, and enterprise architecture best practices while remaining scalable, reliable, and AI-ready.
