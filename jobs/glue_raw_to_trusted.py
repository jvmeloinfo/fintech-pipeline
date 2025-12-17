import sys
from pyspark.sql import SparkSession, functions as F, types as T
from awsglue.utils import getResolvedOptions

def build_spark(app_name="fintech-raw-to-trusted"):
    return SparkSession.builder.appName(app_name).getOrCreate()

def main():
    args = getResolvedOptions(sys.argv, ["raw_base_path", "trusted_base_path"])

    raw_base = args["raw_base_path"].rstrip("/")
    trusted_base = args["trusted_base_path"].rstrip("/")

    spark = build_spark()

    countries = (
        spark.read.option("header", True)
        .csv(f"{raw_base}/countries/")
        .select(
            F.trim("country_code").alias("country_code"),
            F.trim("country").alias("country")
        )
        .dropna(subset=["country_code"])
        .dropDuplicates(["country_code"])
    )

    tx = (
        spark.read.option("header", True)
        .csv(f"{raw_base}/transactions/")
        .select(
            F.trim("country_code").alias("country_code"),
            F.trim("transaction_date").alias("transaction_date"),
            F.trim("bank").alias("bank"),
            F.trim("company").alias("company"),
            F.trim("transaction_id").alias("transaction_id"),
            F.trim("transaction_value").alias("transaction_value"),
            F.trim("payment_due_date").alias("payment_due_date"),
        )
        .dropna(subset=["transaction_id"])
        .dropDuplicates(["transaction_id"])
    )

    tx = (
        tx
        .withColumn("transaction_date", F.to_date("transaction_date"))  # ajuste formato se precisar
        .withColumn("payment_due_date", F.to_date("payment_due_date"))
        .withColumn(
            "transaction_value",
            F.regexp_replace("transaction_value", ",", ".").cast(T.DecimalType(18, 2))
        )
    )

    final_df = (
        tx.join(countries, on="country_code", how="left")
        .withColumn("days_late", F.datediff(F.current_date(), F.col("payment_due_date")))
        .withColumn("is_late", F.when(F.col("days_late") > 0, F.lit(1)).otherwise(F.lit(0)))
        .withColumn("ingestion_date", F.current_date())
    )

    (
        final_df.write.mode("overwrite")
        .format("parquet")
        .partitionBy("ingestion_date")
        .save(f"{trusted_base}/transactions_enriched/")
    )

    spark.stop()

if __name__ == "__main__":
    main()
