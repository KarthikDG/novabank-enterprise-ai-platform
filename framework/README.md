# 🏦 NovaBank Common Frameworks

## Overview

The `framework` module provides reusable enterprise-grade components used across Bronze, Silver, and Gold data pipelines within the NovaBank Enterprise AI Platform.

These frameworks standardize:

- Audit Logging
- Data Quality Validation
- Incremental Processing
- Quarantine Management

Using shared frameworks ensures consistency, governance, and maintainability across Azure Databricks workloads.

---

# 📂 Framework Structure

```text
framework/

├── NB_Audit_Framework.py
├── NB_DQ_Framework.py
├── NB_Watermark_Framework.py
├── NB_Quarantine_Framework.py
└── README.md
```

---

# 🔍 NB_Audit_Framework.py

## Purpose

Provides centralized audit logging for all data pipelines.

Supports:

- Pipeline Execution Logging
- Record Counts
- Success / Failure Status
- Error Messages
- Processing Timestamps

---

## Audit Table

```text
novabank_prod.audit.audit_pipeline_runs
```

---

## Captured Information

| Field | Description |
|---------|-------------|
| pipeline_name | Name of pipeline |
| layer | Bronze / Silver / Gold |
| source_table | Input table |
| target_table | Output table |
| records_processed | Record count |
| status | SUCCESS / FAILED |
| error_message | Exception message |
| audit_timestamp | Processing timestamp |

---

## Example

```python
audit = AuditFramework(
    spark,
    AUDIT_TABLE
)

audit.write_audit_record(
    pipeline_name="NB_Customer360_Gold",
    layer="GOLD",
    source_table=CUSTOMER_TABLE,
    target_table=TARGET_TABLE,
    records_processed=1000,
    status="SUCCESS"
)
```

---

# ✅ NB_DQ_Framework.py

## Purpose

Provides reusable Data Quality checks.

Supports:

- Null Validation
- Duplicate Validation
- Negative Value Detection
- Required Column Validation

---

## Available Functions

### Check Null Values

```python
dq.check_nulls(
    df,
    "CustomerID"
)
```

---

### Check Duplicate Records

```python
dq.check_duplicates(
    df,
    "CustomerID"
)
```

---

### Check Negative Values

```python
dq.check_negative_values(
    df,
    "TransactionAmount"
)
```

---

### Validate Required Columns

```python
dq.validate_required_columns(
    df,
    [
        "CustomerID",
        "TransactionAmount"
    ]
)
```

---

## Typical Usage

```python
dq = DataQualityFramework()

dq.validate_required_columns(
    customer_df,
    required_columns
)
```

---

# ⏱ NB_Watermark_Framework.py

## Purpose

Enables incremental processing using watermark values.

Supports:

- Incremental Loads
- Delta Processing
- CDC Style Processing
- Reduced Pipeline Cost

---

## Watermark Table

```text
novabank_prod.control.pipeline_watermarks
```

---

## Watermark Structure

| Field | Description |
|---------|-------------|
| pipeline_name | Pipeline Name |
| watermark_value | Max Processed Value |
| updated_timestamp | Last Update |

---

## Retrieve Watermark

```python
watermark = (
    watermark_framework
    .get_watermark(
        "customer360_gold"
    )
)
```

---

## Update Watermark

```python
watermark_framework.update_watermark(
    pipeline_name="customer360_gold",
    watermark_value=max_date
)
```

---

## Example Use Case

```python
transaction_df = (
    transaction_df
    .filter(
        F.col("TransactionDate")
        > watermark
    )
)
```

---

# 🚨 NB_Quarantine_Framework.py

## Purpose

Captures invalid records without failing the entire pipeline.

Supports:

- Invalid Data Isolation
- Auditability
- Regulatory Traceability
- Data Stewardship

---

## Quarantine Table

```text
novabank_prod.audit.quarantine_records
```

---

## Captured Fields

| Field | Description |
|---------|-------------|
| Original Record | Source Data |
| quarantine_reason | Why record failed |
| quarantine_timestamp | Capture Time |

---

## Quarantine Example

```python
quarantine.quarantine_records(
    invalid_records_df,
    "Invalid Risk Score"
)
```

---

## Separate Valid and Invalid Records

```python
valid_df, invalid_df = (
    quarantine.filter_valid_records(
        dataframe=df,
        filter_condition=
        (F.col("RiskScore") >= 0)
        &
        (F.col("RiskScore") <= 100)
    )
)
```

---

# 🏗 Framework Architecture

```text
Source Data
      │
      ▼

NB_DQ_Framework

      │

      ├──────────────►
      │               Invalid Records
      │
      ▼

NB_Quarantine_Framework

      │
      ▼

Transformations

      │
      ▼

NB_Watermark_Framework

      │
      ▼

Target Delta Table

      │
      ▼

NB_Audit_Framework

      │
      ▼

Audit Logs
```

---

# 🔒 Governance Benefits

The framework layer provides:

✅ Standardized Logging

✅ Data Quality Enforcement

✅ Incremental Processing

✅ Invalid Data Isolation

✅ Auditability

✅ Reusability

✅ Regulatory Compliance

✅ Reduced Maintenance Effort

---

# 📈 Usage Across Platform

| Domain | Uses Frameworks |
|----------|----------|
| Customer360 | ✅ |
| Fraud Analytics | ✅ |
| Risk Analytics | ✅ |
| MLOps | ✅ |
| GenAI | ✅ |
| Power BI Datasets | ✅ |

---

# 🎯 Design Principles

The NovaBank framework layer follows:

- Reusability
- Modularity
- Scalability
- Observability
- Auditability
- Security
- Governance

These building blocks ensure a consistent implementation pattern across all enterprise data, AI, and analytics workloads.
