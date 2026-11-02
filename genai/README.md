# Generative AI Platform

## Overview

The NovaBank Generative AI Platform enables secure, enterprise-grade AI capabilities using Azure OpenAI, Retrieval Augmented Generation (RAG), Vector Search, and AI Agents.

The platform helps business users, risk analysts, fraud investigators, customer service agents, and relationship managers interact with enterprise knowledge using natural language.

---

# Objectives

The GenAI platform supports:

- Natural Language Search
- Knowledge Discovery
- Customer Summaries
- Fraud Investigations
- Risk Analysis
- Policy Assistance
- Regulatory Compliance Support
- AI Agent Automation

---

# High-Level Architecture

```text
Documents
Policies
Procedures
KYC Records
Fraud Cases
Risk Reports
Customer Data

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

Vector Database

       │
       ▼

Azure OpenAI

       │
       ▼

AI Application
```

---

# Folder Structure

```text
genai/

├── README.md

├── rag/

├── embeddings/

├── vector-search/

├── prompts/

├── agents/

├── evaluation/

└── applications/
```

---

# Business Use Cases

## Relationship Manager Assistant

Questions:

```text
Summarise customer profile

Show customer risk exposure

Show customer products

Summarise customer interactions
```

---

## Fraud Investigation Assistant

Questions:

```text
Explain this fraud alert

Show fraud history

Summarise suspicious transactions

Generate investigation summary
```

---

## Compliance Assistant

Questions:

```text
What are KYC requirements?

What documents are mandatory?

Summarise AML controls

Explain customer onboarding process
```

---

## Risk Assistant

Questions:

```text
Show customer risk score

Explain risk rating

Summarise exposure

Show recent risk events
```

---

# Retrieval Augmented Generation (RAG)

The platform uses RAG to ground AI responses using enterprise knowledge.

Workflow:

```text
User Question

     │

     ▼

Embedding Search

     │

     ▼

Vector Retrieval

     │

     ▼

Relevant Context

     │

     ▼

Azure OpenAI Response
```

Benefits:

```text
Higher Accuracy

Reduced Hallucinations

Traceable Sources

Enterprise Knowledge Reuse
```

---

# Embeddings

Supported Document Types:

```text
PDF

Word

Email

Policy

Procedure

Knowledge Base

Fraud Reports

Risk Reports
```

Stored As:

```text
Vector Embeddings
```

---

# Vector Search

Stores:

```text
Document Chunks

Embeddings

Metadata
```

Typical Metadata:

```text
Document Name

Source System

Author

Creation Date

Classification
```

---

# Prompt Engineering

Prompt Templates Include:

```text
Customer Summary Prompt

Fraud Analysis Prompt

Risk Assessment Prompt

Compliance Prompt
```

Goals:

```text
Consistent Responses

Better Accuracy

Lower Cost

Improved Explainability
```

---

# AI Agents

## Fraud Agent

Responsibilities:

```text
Fraud Alert Investigation

Case Summarisation

Transaction Analysis
```

---

## Customer Agent

Responsibilities:

```text
Customer 360

Product Recommendations

Customer Insights
```

---

## Risk Agent

Responsibilities:

```text
Risk Analysis

Exposure Reporting

Risk Explanations
```

---

## Compliance Agent

Responsibilities:

```text
Policy Search

KYC Guidance

AML Assistance
```

---

# Security

Implemented Controls:

```text
Azure Entra ID

RBAC

Managed Identity

Data Masking

Audit Logging

Content Filtering
```

---

# Governance

The platform enforces:

```text
Data Classification

Prompt Tracking

Response Auditing

Model Versioning

User Access Controls
```

---

# Evaluation

Models are evaluated using:

```text
Answer Correctness

Grounding Quality

Source Attribution

Latency

User Feedback
```

---

# Monitoring

Track:

```text
Prompt Volume

Response Latency

Token Usage

Retrieval Accuracy

Error Rates
```

---

# Technology Stack

```text
Azure OpenAI

Databricks

Vector Search

MLflow

Azure Key Vault

Azure Monitor

Azure AI Services
```

---

# Future Components

```text
rag/

Build_RAG_Pipeline.py

embeddings/

Generate_Embeddings.py

vector-search/

Create_Vector_Index.py

agents/

Fraud_Investigation_Agent.py

Customer360_Agent.py

Risk_Assistant_Agent.py
```

---

# Success Metrics

```text
Grounded Responses > 95%

Response Time < 3 Seconds

Hallucination Rate < 2%

Citation Accuracy > 95%
```

This GenAI platform enables scalable AI-powered banking experiences built on trusted enterprise data and governed knowledge assets.
