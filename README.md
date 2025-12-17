# Fintech Data Pipeline

Pipeline de dados para ingestão, processamento e análise de transações financeiras.

## Arquitetura
S3 (Raw) → AWS Glue (PySpark) → S3 (Parquet) → Glue Catalog → Athena / BI
