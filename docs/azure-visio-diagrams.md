# NovaBank Enterprise AI Platform
# Azure Visio / Draw.io / Lucidchart Diagrams

---

# Purpose

This document provides professional Azure architecture layouts that can be recreated using:

```text
Microsoft Visio

Draw.io

Lucidchart

PowerPoint

Miro

Figma
```

The layouts follow Microsoft Cloud Adoption Framework and Azure Architecture Center design principles.

---

# Diagram 1: Executive Architecture Overview

## Azure Icons Required

```text
Azure Data Factory

Azure Event Hub

Azure Data Lake Storage Gen2

Azure Databricks

Azure OpenAI

Power BI

Key Vault

Azure Monitor
```

## Layout

```text
┌──────────────────────────────────────────┐
│              Source Systems              │
└──────────────────────────────────────────┘

Core Banking
Payments
CRM
AML
KYC

                  │
                  ▼

┌──────────────────────────────────────────┐
│ Azure Data Factory                       │
└──────────────────────────────────────────┘

                  │

                  ▼

┌──────────────────────────────────────────┐
│ Azure Event Hub                          │
└──────────────────────────────────────────┘

                  │

                  ▼

┌──────────────────────────────────────────┐
│ Azure Data Lake Storage Gen2             │
└──────────────────────────────────────────┘

     Bronze
     Silver
     Gold

                  │

                  ▼

┌──────────────────────────────────────────┐
│ Azure Databricks                         │
└──────────────────────────────────────────┘

                  │

      ┌───────────┼─────────────┐

      ▼           ▼             ▼

  Power BI     MLflow      Azure OpenAI
```

---

# Diagram 2: Azure Landing Zone

```text
Management Group
        │
        ▼

NovaBank

├── Platform Subscription

├── Data Subscription

├── AI Subscription

└── Shared Services
```

Inside Data Subscription:

```text
Resource Group

├── ADF

├── Databricks

├── Storage

├── Event Hub

├── Key Vault

└── Azure Monitor
```

---

# Diagram 3: Networking Architecture

```text
Virtual Network

├────────────────────────────┤

Databricks Public Subnet

Databricks Private Subnet

Private Endpoint Subnet

Monitoring Subnet

├────────────────────────────┤

Private Endpoints

ADLS

Key Vault

Azure OpenAI

Databricks
```

Recommended colors:

```text
Blue = Application

Green = Data

Red = Security

Orange = Monitoring
```

---

# Diagram 4: Medallion Architecture

```text
                 Sources

                   │

                   ▼

┌──────────────────────────────┐
│ Bronze Layer                 │
│ Raw Data                     │
└──────────────────────────────┘

                   │

                   ▼

┌──────────────────────────────┐
│ Silver Layer                 │
│ Cleansed & Enriched Data     │
└──────────────────────────────┘

                   │

                   ▼

┌──────────────────────────────┐
│ Gold Layer                   │
│ Business Models              │
└──────────────────────────────┘

                   │

                   ▼

Business Consumption
```

Use separate Azure Storage icons for:

```text
bronze

silver

gold
```

---

# Diagram 5: Data Factory Architecture

```text
Metadata Table

       │

       ▼

Lookup Activity

       │

       ▼

ForEach Loop

       │

       ▼

Copy Activities

       │

       ▼

ADLS Bronze

       │

       ▼

Databricks
```

Icons:

```text
ADF Pipeline

Azure SQL

Data Lake

Databricks
```

---

# Diagram 6: Event Streaming Architecture

```text
Transaction Events

ATM Events

Card Events

Mobile Events

      │

      ▼

Azure Event Hub

      │

      ▼

Databricks Streaming

      │

      ▼

Silver Layer

      │

      ▼

Fraud Analytics
```

Icons:

```text
Event Hub

Databricks

Delta Lake
```

---

# Diagram 7: Customer360 Architecture

```text
Customer Master
        │

Products
        │

Transactions
        │

Fraud Data
        │

Risk Data
        │

        ▼

Customer360 Gold

        │

 ┌──────┼───────────┐

 ▼      ▼           ▼

Power BI

Customer Agent

Relationship Manager
```

Suggested center icon:

```text
Gold Database
```

---

# Diagram 8: Fraud Analytics Architecture

```text
Transactions

      │

      ▼

Fraud Signals

      │

      ▼

Feature Engineering

      │

      ▼

ML Model

      │

      ▼

Fraud Cases

      │

      ▼

Power BI Dashboard
```

Icons:

```text
Databricks

MLflow

Power BI
```

---

# Diagram 9: MLOps Architecture

```text
Feature Store

       │

       ▼

Training

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

Azure Icons:

```text
Databricks

MLflow

Model Serving

Azure Monitor
```

---

# Diagram 10: Generative AI Architecture

```text
Policies

Procedures

Fraud Reports

Risk Reports

      │

      ▼

Document Ingestion

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

Answer
```

Icons:

```text
Storage

Azure OpenAI

Vector Search

AI Agent
```

---

# Diagram 11: RAG Architecture

```text
User Question

      │

      ▼

Embedding Generator

      │

      ▼

Vector Search

      │

      ▼

Top Documents

      │

      ▼

Prompt Builder

      │

      ▼

GPT-4o

      │

      ▼

Response
```

---

# Diagram 12: Security Architecture

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

Audit Logs
```

Icons:

```text
Entra ID

Key Vault

Private Endpoint

Security Center
```

---

# Diagram 13: Monitoring Architecture

```text
ADF

Databricks

ML Models

GenAI

Infrastructure

      │

      ▼

Azure Monitor

      │

      ▼

Log Analytics

      │

      ▼

Action Groups

      │

      ▼

Operations Team
```

---

# Diagram 14: CI/CD Architecture

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

# Diagram 15: Enterprise Executive View

```text
ADF + Event Hub

       │

       ▼

ADLS

       │

       ▼

Databricks

       │

       ▼

dbt

       │

       ▼

Gold Models

 ┌────────┼────────┬────────┐

 ▼        ▼        ▼        ▼

Power BI

Customer360

MLflow

Azure OpenAI
```

---

# Presentation Recommendation

For interviews, keep a slide deck with:

```text
Slide 1 - High Level Architecture

Slide 2 - Medallion Architecture

Slide 3 - Customer360

Slide 4 - Fraud Analytics

Slide 5 - MLOps

Slide 6 - GenAI & RAG

Slide 7 - Security

Slide 8 - CI/CD

Slide 9 - Monitoring

Slide 10 - Business Outcomes
```

These diagrams can be recreated visually using official Azure architecture icons and are suitable for portfolio presentations, interviews, architecture reviews, and client demonstrations.
