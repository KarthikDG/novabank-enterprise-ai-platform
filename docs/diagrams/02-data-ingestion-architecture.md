# Azure Data Factory Architecture

```text
Metadata Table
     A great addition would be a dedicated architecture diagrams document.

### File: `docs/azure-architecture-diagrams.md`

Create:

```text
docs/azure-architecture-diagrams.md
```

Paste the following:

````markdown
# NovaBank Enterprise AI Platform
# Azure Architecture Diagrams

---

# 1. High-Level Enterprise Architecture

```text
┌─────────────────────────────────────────────┐
│             Source Systems                  │
├─────────────────────────────────────────────┤
│ Core Banking                                │
│ CRM                                         │
│ Payments                                    │
│ ATM                                         │
│ Mobile Banking                              │
│ KYC / AML                                   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼

┌─────────────────────────────────────────────┐
│ Azure Data Factory                          │
│ Azure Event Hub                             │
└─────────────────┬───────────────────────────┘
                  │
                  ▼

┌─────────────────────────────────────────────┐
│ Azure Data Lake Storage Gen2                │
│ Bronze Layer                                │
└─────────────────┬───────────────────────────┘
                  │
                  ▼

┌─────────────────────────────────────────────┐
│ Azure Databricks                            │
│ Bronze Processing                           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼

┌─────────────────────────────────────────────┐
│ Silver Layer                                │
└─────────────────┬───────────────────────────┘
                  │
                  ▼

┌─────────────────────────────────────────────┐
│ dbt Analytics Engineering                   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼

┌─────────────────────────────────────────────┐
│ Gold Layer                                  │
└──────────────┬──────────────┬───────────────┘
               │              │
               ▼              ▼

         Power BI      ML + GenAI
```

---

# 2. Azure Resource Architecture

```text
Azure Subscription
│
├── Resource Group
│
├── Azure Data Factory
│
├── Azure Databricks
│
├── Azure Data Lake Gen2
│
├── Azure Event Hub
│
├── Azure Key Vault
│
├── Log Analytics
│
├── Azure Monitor
│
└── Application Insights
```

---

# 3. Medallion Architecture

```text
             Raw Sources
                   │
                   ▼

┌──────────────────────────────┐
│ Bronze Layer                 │
│ Raw Data                     │
│ Historical Data              │
└────────────┬─────────────────┘
             │
             ▼

┌──────────────────────────────┐
│ Silver Layer                 │
│ Cleansed Data                │
│ Validated Data               │
│ Enriched Data                │
└────────────┬─────────────────┘
             │
             ▼

┌──────────────────────────────┐
│ Gold Layer                   │
│ Customer360                  │
│ Fraud Analytics              │
│ Risk Analytics               │
└────────────┬─────────────────┘
             │
             ▼

Business Consumption
```

---

# 4. Azure Data Factory Architecture

```text
Metadata Table
       │
       ▼

Lookup Activity
       │
       ▼

ForEach Source
       │
       ▼

Copy Activity
       │
       ▼

Bronze Layer
       │
       ▼

Audit Logging
```

---

# 5. Streaming Architecture

```text
ATM Events
Payment Events
Mobile Events
Fraud Events
        │
        ▼

Azure Event Hub

        │
        ▼

Structured Streaming

        │
        ▼

Databricks

        │
        ▼

Silver Tables

        │
        ▼

Fraud Analytics
```

---

# 6. Customer360 Architecture

```text
Customer Master
        │

Transactions
        │

Products
        │

Risk Scores
        │

Fraud Signals
        │
        ▼

Customer360 Model

        │
        ▼

Power BI
Customer Agent
Relationship Manager
```

---

# 7. Fraud Analytics Architecture

```text
Transactions

      │
      ▼

Fraud Rules

      │
      ▼

Fraud Features

      │
      ▼

ML Model

      │
      ▼

Fraud Score

      │
      ▼

Investigation Queue
```

---

# 8. MLflow MLOps Architecture

```text
Gold Layer

    │
    ▼

Feature Engineering

    │
    ▼

Model Training

    │
    ▼

MLflow Tracking

    │
    ▼

Model Registry

    │
    ▼

Deployment

    │
    ▼

Monitoring
```

---

# 9. Generative AI Architecture

```text
Documents

Policies

Procedures

Fraud Reports

Risk Reports

       │
       ▼

Chunking

       │
       ▼

Embeddings

       │
       ▼

Vector Search

       │
       ▼

Azure OpenAI

       │
       ▼

AI Response
```

---

# 10. RAG Architecture

```text
User Question

      │
      ▼

Generate Embedding

      │
      ▼

Vector Search

      │
      ▼

Retrieve Documents

      │
      ▼

Build Context

      │
      ▼

Azure OpenAI

      │
      ▼

Grounded Response
```

---

# 11. AI Agents Architecture

```text
                    Azure OpenAI
                           │
                           ▼

┌──────────────┬──────────────┬──────────────┐

Fraud Agent   Customer360    Risk Agent
                  Agent

└──────────────┴──────────────┴──────────────┘
                   │
                   ▼

               RAG Layer

                   │
                   ▼

         Enterprise Knowledge Base
```

---

# 12. Security Architecture

```text
Users
   │
   ▼

Microsoft Entra ID

   │
   ▼

MFA

   │
   ▼

RBAC

   │
   ▼

Applications

   │
   ▼

Data Platform

   │
   ▼

Audit Logging
```

---

# 13. Network Architecture

```text
Virtual Network

├── Databricks Subnet

├── Private Endpoint Subnet

├── ADF Managed VNET

└── Monitoring Services


Private Endpoints

├── ADLS

├── Key Vault

├── Databricks

└── Azure OpenAI
```

---

# 14. CI/CD Architecture

```text
Developer

    │
    ▼

GitHub

    │
    ▼

Pull Request

    │
    ▼

Azure DevOps

    │
    ▼

Build Pipeline

    │
    ▼

Release Pipeline

    │
    ▼

DEV

TEST

UAT

PROD
```

---

# 15. Complete End-to-End Platform Diagram

```text
 Sources
    │
    ▼

ADF + Event Hub
    │
    ▼

ADLS Bronze
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
 ┌──┼───────────────┬───────────────┐
 ▼  ▼               ▼               ▼

Power BI      MLflow       Azure OpenAI

                             │
                             ▼

                       AI Agents

                             │
                             ▼

                      Business Users
```
