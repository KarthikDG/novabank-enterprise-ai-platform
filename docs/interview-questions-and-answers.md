# NovaBank Enterprise AI Platform
# Interview Questions & Answers

## Introduction

This guide contains project-specific interview questions and model answers covering:

- Azure Data Factory
- Databricks
- Delta Lake
- dbt
- Azure Event Hub
- MLflow
- Azure OpenAI
- Terraform
- CI/CD
- Security
- Architecture

---

# Architecture Questions

## Q1. Explain the overall architecture.

### Answer

The platform follows a modern Azure Lakehouse architecture.

```text
Source Systems
     │
     ▼
ADF + Event Hub
     │
     ▼
ADLS Gen2
     │
     ▼
Databricks Bronze
     │
     ▼
Databricks Silver
     │
     ▼
dbt Gold Models
     │
 ┌───┼─────────┐
 ▼   ▼         ▼

Power BI  MLflow  Azure OpenAI
```

The architecture supports Customer 360, Fraud Analytics, Risk Analytics, MLOps, and GenAI use cases.

---

## Q2. Why did you choose a Lakehouse architecture?

### Answer

A Lakehouse combines:

```text
Data Lake Scalability

Data Warehouse Reliability
```

Benefits:

- Lower Cost
- Open Formats
- ACID Transactions
- Advanced Analytics
- Machine Learning Support

---

## Q3. Why did you choose Azure?

### Answer

Because Azure provides:

```text
ADF
Databricks
ADLS
Event Hub
Azure OpenAI
Power BI
```

in a tightly integrated ecosystem.

---

# Azure Data Factory Questions

## Q4. What is the purpose of Azure Data Factory?

### Answer

ADF is the enterprise ingestion service.

Responsibilities:

```text
Batch Loads

Incremental Loads

Scheduling

Pipeline Orchestration

Monitoring
```

---

## Q5. How did you implement incremental loads?

### Answer

Using watermark columns.

Example:

```sql
SELECT *
FROM Transactions
WHERE LastModifiedDate >
      LastProcessedValue
```

Only changed data is loaded.

---

## Q6. What is a metadata-driven pipeline?

### Answer

A framework where source information is stored in control tables.

Example:

```text
Source System

Source Table

Load Type

Watermark Column
```

A single pipeline dynamically processes multiple sources.

---

## Q7. Difference between Lookup and Get Metadata?

### Answer

Lookup:

```text
Reads Data
```

Get Metadata:

```text
Reads File Metadata
```

---

## Q8. How do you handle failures?

### Answer

Implemented:

```text
Retry Logic

Error Logging

Quarantine Layer

Monitoring Alerts
```

---

# Databricks Questions

## Q9. Why Databricks?

### Answer

Provides:

```text
Spark Processing

Delta Lake

Streaming

MLflow

Unity Catalog
```

at enterprise scale.

---

## Q10. What are Bronze, Silver and Gold?

### Answer

### Bronze

```text
Raw Data
```

### Silver

```text
Validated Data
```

### Gold

```text
Business Data
```

---

## Q11. What is Unity Catalog?

### Answer

Central governance layer.

Provides:

```text
Data Lineage

RBAC

Data Discovery

Auditing
```

---

## Q12. What is OPTIMIZE?

### Answer

Compacts small Delta files.

```sql
OPTIMIZE table_name
```

Improves query performance.

---

## Q13. What is ZORDER?

### Answer

Improves data skipping.

```sql
OPTIMIZE table_name
ZORDER BY(customer_id)
```

---

## Q14. What is Structured Streaming?

### Answer

Real-time processing engine in Spark.

Used for:

```text
Fraud Detection

Event Processing

Monitoring
```

---

# Delta Lake Questions

## Q15. What is Delta Lake?

### Answer

An open table format providing:

```text
ACID Transactions

Time Travel

Schema Evolution

Version Control
```

---

## Q16. What is Time Travel?

### Answer

Access previous table versions.

Example:

```sql
SELECT *
FROM table VERSION AS OF 5
```

---

## Q17. What is Schema Evolution?

### Answer

Allows new columns without rebuilding tables.

---

# dbt Questions

## Q18. Why use dbt?

### Answer

To manage:

```text
Business Logic

Testing

Documentation

Lineage
```

separately from engineering pipelines.

---

## Q19. Difference between ref() and source()?

### Answer

ref():

```sql
{{ ref('dim_customer') }}
```

Refers to dbt models.

source():

```sql
{{ source('customer','customer_silver') }}
```

Refers to external tables.

---

## Q20. What are dbt tests?

### Answer

Quality checks:

```text
Unique

Not Null

Accepted Values

Relationships
```

---

# Event Hub Questions

## Q21. Why Event Hub?

### Answer

Supports:

```text
High Throughput

Streaming

Real-Time Events
```

Used for transaction and fraud events.

---

## Q22. Event Hub vs Service Bus?

### Answer

Event Hub:

```text
Streaming Platform
```

Service Bus:

```text
Messaging Platform
```

---

# Customer 360 Questions

## Q23. What is Customer 360?

### Answer

Unified customer view containing:

```text
Transactions

Products

Fraud Data

Risk Data

Customer Profile
```

---

## Q24. Business value of Customer 360?

### Answer

Provides:

```text
Better Service

Personalization

Cross-Sell Opportunities

Risk Visibility
```

---

# Fraud Analytics Questions

## Q25. How does fraud scoring work?

### Answer

Combines:

```text
Transaction Value

Fraud Signals

Historical Behaviour

Risk Attributes
```

to calculate fraud scores.

---

## Q26. What is a fraud feature?

### Answer

A predictive variable.

Example:

```text
High Transaction Amount

Country Change

Unusual Frequency
```

---

# Risk Analytics Questions

## Q27. How is risk calculated?

### Answer

Uses:

```text
Exposure

Fraud History

Transaction Behaviour

Customer Segment
```

to derive enterprise risk scores.

---

## Q28. High-risk customer example?

### Answer

Customer with:

```text
Large Exposure

Multiple Fraud Signals

High Transaction Activity
```

---

# MLflow Questions

## Q29. Why MLflow?

### Answer

Supports:

```text
Experiment Tracking

Model Registry

Model Deployment

Monitoring
```

---

## Q30. What is Model Registry?

### Answer

Central location for storing model versions.

Stages:

```text
Development

Staging

Production
```

---

# Generative AI Questions

## Q31. What is RAG?

### Answer

Retrieval Augmented Generation combines:

```text
Search

Knowledge Retrieval

LLM Generation
```

to produce grounded answers.

---

## Q32. Why use RAG?

### Answer

Reduces hallucinations.

Provides:

```text
Source Attribution

Higher Accuracy

Enterprise Knowledge Access
```

---

## Q33. What are embeddings?

### Answer

Numeric vector representations of text.

Used for:

```text
Similarity Search

Vector Search

Document Retrieval
```

---

## Q34. What is Vector Search?

### Answer

Searches documents using embeddings rather than keywords.

---

## Q35. What AI Agents did you build?

### Answer

```text
Fraud Investigation Agent

Customer360 Agent

Risk Assistant Agent
```

---

# Terraform Questions

## Q36. Why Terraform?

### Answer

Infrastructure as Code.

Benefits:

```text
Repeatability

Version Control

Automation

Auditability
```

---

## Q37. What resources are deployed?

### Answer

```text
ADF

Databricks

Storage

Key Vault

Event Hub

Monitoring
```

---

# Security Questions

## Q38. How is security implemented?

### Answer

Implemented:

```text
Entra ID

RBAC

Key Vault

Managed Identity

Private Endpoints

Unity Catalog
```

---

## Q39. Why Managed Identity?

### Answer

Eliminates password management.

Provides secure service authentication.

---

## Q40. How is sensitive data protected?

### Answer

Using:

```text
Encryption

Data Masking

RBAC

Private Networking
```

---

# CI/CD Questions

## Q41. How are deployments automated?

### Answer

Using:

```text
GitHub

Azure DevOps

Terraform

Release Pipelines
```

---

## Q42. Deployment Flow?

### Answer

```text
Developer

▼

Pull Request

▼

CI Validation

▼

CD Deployment

▼

DEV

TEST

UAT

PROD
```

---

# Monitoring Questions

## Q43. What monitoring tools are used?

### Answer

```text
Azure Monitor

Log Analytics

Application Insights
```

---

## Q44. What do you monitor?

### Answer

```text
Pipeline Failures

Databricks Jobs

Model Drift

GenAI Services

Infrastructure
```

---

# Final Interview Question

## Q45. Summarize the project in 60 seconds.

### Answer

"I designed an enterprise Azure Lakehouse platform using Azure Data Factory, Azure Databricks, ADLS Gen2, dbt, MLflow, Azure OpenAI, and Power BI. The platform supports Customer 360, Fraud Analytics, Risk Analytics, MLOps, and Generative AI use cases. It follows Medallion Architecture, uses Delta Lake and Unity Catalog for governance, Terraform and Azure DevOps for CI/CD, and incorporates enterprise-grade security, monitoring, and compliance controls."
