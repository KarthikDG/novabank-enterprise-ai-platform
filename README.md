# Novabank Enterprise AI Risk & Fraud Intelligence Platform

## Overview

This repository contains a reference implementation of an enterprise-scale Data, AI, Fraud Detection, Risk Analytics, and GenAI platform designed for a modern banking environment.

## Technology Stack

- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- Delta Lake
- dbt Core
- MLflow
- Azure OpenAI
- Unity Catalog
- Power BI
- Azure DevOps
- Terraform

## Repository Structure

```text
rabobank-enterprise-ai-platform/
├── docs/
├── terraform/
├── adf/
├── databricks/
├── dbt/
├── mlops/
├── streaming/
├── genai/
├── monitoring/
├── powerbi/
└── cicd/
```

## Business Goals

- Fraud Detection
- Risk Analytics
- Customer 360
- Regulatory Compliance
- AI and GenAI Enablement

## Architecture

Source Systems -> ADF -> ADLS Bronze -> Databricks -> Silver -> dbt -> Gold -> Power BI / ML / GenAI

## Security

- RBAC
- Encryption
- Unity Catalog
- Row Level Security
- Column Level Security

## CI/CD

Azure DevOps + Terraform + Databricks Asset Bundles
