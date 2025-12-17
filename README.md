Fintech Data Pipeline – AWS Glue & Data Lake
 Visão Geral
Este projeto implementa um pipeline de dados completo em nuvem AWS, simulando um cenário real de uma fintech que recebe diariamente arquivos CSV contendo informações de transações financeiras e dados de países, armazenados em um bucket S3 de outra conta AWS (cross-account).
A solução realiza a ingestão, tratamento, enriquecimento, armazenamento e disponibilização para consulta SQL, aplicando boas práticas de Engenharia de Dados, com foco em escalabilidade, governança e segurança.
Objetivo do Projeto
Construir um pipeline capaz de:
Ingerir dados CSV de um bucket S3 em outra conta AWS
Armazenar os dados brutos em uma camada RAW
Processar, limpar e enriquecer os dados
Persistir os dados tratados em formato Parquet particionado
Registrar o dataset no AWS Glue Data Catalog
Disponibilizar os dados para consulta via Amazon Athena
Arquitetura da Solução
┌──────────────────────────┐
│   Conta AWS Externa      │
│  (Source - S3 CSV)       │
│  upload-andressa         │
└────────────┬─────────────┘
             │ (Cross-account IAM Role)
             ▼
┌──────────────────────────┐
│     S3 RAW (Target)      │
│   raw-jvmelo/fintech     │
└────────────┬─────────────┘
             │ Glue Job (Spark)
             ▼
┌──────────────────────────┐
│   S3 TRUSTED (Parquet)   │
│ trusted-jvmelo/fintech   │
└────────────┬─────────────┘
             │ Glue Crawler
             ▼
┌──────────────────────────┐
│  Glue Data Catalog       │
│  Database: fintech_trusted│
└────────────┬─────────────┘
             ▼
        Amazon Athena
📂 Estrutura do Data Lake
RAW
Dados ingeridos sem transformação, mantendo o formato CSV.
s3://raw-jvmelo/fintech/
├── countries/
│   └── part-*.csv
└── transactions/
    └── part-*.csv
TRUSTED
Dados tratados, enriquecidos e otimizados para consulta analítica.
s3://trusted-jvmelo/fintech/
└── transactions_enriched/
    ├── ingestion_date=YYYY-MM-DD/
    │   └── part-*.snappy.parquet
Dados de Entrada
countries
Campo	Tipo
country_code	string
country	string
transactions
Campo	Tipo
country_code	string
transaction_date	date
bank	string
company	string
transaction_id	string
transaction_value	decimal
payment_due_date	date
Pipeline de Processamento
Ingestão RAW (Cross-account)
Glue Job lê arquivos CSV de um bucket S3 em outra conta AWS
Escrita na camada RAW mantendo o formato original
Processamento RAW ➜ TRUSTED
Limpeza de dados (trim, remoção de nulos)
Deduplicação por chaves de negócio
Conversão de tipos (datas, valores monetários)
Enriquecimento com:
Nome do país
Indicadores de atraso (days_late, is_late)
ingestion_date
Escrita em Parquet particionado
Catalogação
Glue Crawler registra automaticamente a tabela no Glue Data Catalog
Enriquecimentos Aplicados
Campos adicionais criados:
Campo	Descrição
country	Nome do país
days_late	Dias de atraso do pagamento
is_late	Indicador de atraso (0/1)
ingestion_date	Data de ingestão
Tecnologias Utilizadas
Amazon S3 – Data Lake
AWS Glue (Spark) – Processamento ETL
AWS Glue Crawler – Catalogação automática
AWS Glue Data Catalog
Amazon Athena – Consulta SQL
IAM (Least Privilege + Cross-account)
Apache Spark (PySpark)
Segurança e Governança
Acesso cross-account via IAM Role
Políticas seguindo princípio do menor privilégio
Separação clara entre camadas RAW e TRUSTED
Dados particionados para melhor performance e custo

Exemplos de Consultas (Athena)
Países com mais transações
SELECT country, COUNT(*) AS total_transactions
FROM fintech_trusted.transactions_enriched
GROUP BY country
ORDER BY total_transactions DESC;
Bancos com mais transações
SELECT bank, COUNT(*) AS total
FROM fintech_trusted.transactions_enriched
GROUP BY bank
ORDER BY total DESC;
Transações atrasadas
SELECT *
FROM fintech_trusted.transactions_enriched
WHERE is_late = 1;

Como Executar
Executar o Glue Job de ingestão RAW
Executar o Glue Job glue_raw_to_trusted
Executar o Glue Crawler
Consultar os dados via Amazon Athena

Considerações Finais
Este projeto demonstra um pipeline de dados completo, seguindo padrões utilizados em ambientes corporativos reais:
Data Lake em camadas
ETL escalável
Governança e segurança
Pronto para consumo analítico
A arquitetura pode ser facilmente estendida para:
Incremental loading
Orquestração com Step Functions
Monitoramento com CloudWatch
Integração com ferramentas de BI
Autor: João Vitor Melo
Ano: 2025
Perfil: Engenheiro de Dados / BI / AWS