import sys
from pyspark.sql import SparkSession
from pyspark.sql import types as T
from awsglue.utils import getResolvedOptions


def build_spark(app_name="fintech-raw-ingestion"):
    return SparkSession.builder.appName(app_name).getOrCreate()


def read_csv(spark, path, schema):
    return (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(path)
    )


def write_csv(df, path):
    (
        df.write
        .mode("overwrite")
        .option("header", True)
        .csv(path)
    )


def main():
    args = getResolvedOptions(
        sys.argv,
        ["countries_src", "transactions_src", "raw_base_path"]
    )

    spark = build_spark()

    countries_schema = T.StructType([
        T.StructField("country_code", T.StringType(), True),
        T.StructField("country", T.StringType(), True),
    ])

    transactions_schema = T.StructType([
        T.StructField("country_code", T.StringType(), True),
        T.StructField("transaction_date", T.StringType(), True),
        T.StructField("bank", T.StringType(), True),
        T.StructField("company", T.StringType(), True),
        T.StructField("transaction_id", T.StringType(), True),
        T.StructField("transaction_value", T.StringType(), True),
        T.StructField("payment_due_date", T.StringType(), True),
    ])

    countries_df = read_csv(spark, args["countries_src"], countries_schema)
    transactions_df = read_csv(spark, args["transactions_src"], transactions_schema)

    write_csv(countries_df, f"{args['raw_base_path']}/countries/")
    write_csv(transactions_df, f"{args['raw_base_path']}/transactions/")

    spark.stop()


if __name__ == "__main__":
    main()
