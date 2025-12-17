# Fintech Data Pipeline

## Objetivo
Pipeline de dados para ingestão, processamento e análise de transações financeiras.

## Arquitetura Proposta (AWS)
- S3 (raw)
- AWS Glue (ETL)
- S3 (processed / curated)
- Athena (consulta)
- BI (QuickSight / Power BI)

## Execução Local
python jobs/glue_etl_transactions.py

## Adaptação para AWS
- Glue Job PySpark
- IAM Role
- Cross-account S3 access
- Athena external table
