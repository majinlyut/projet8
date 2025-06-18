from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.types import StructType, StringType, IntegerType
import os

#  Création de la session Spark avec le connecteur Kafka
spark = SparkSession.builder \
    .appName("RedpandaTicketConsumer") \
    .config("spark.jars", "/opt/bitnami/spark/jars/*") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

#  Schéma des tickets
schema = StructType() \
    .add("ticket_id", IntegerType()) \
    .add("client_id", IntegerType()) \
    .add("created_at", StringType()) \
    .add("demande", StringType()) \
    .add("type", StringType()) \
    .add("priorité", StringType())

#  Lecture du topic Kafka (Redpanda)
kafka_broker = os.getenv("KAFKA_BROKER", "redpanda-0:9092")

raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", "client_tickets") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

#  Parsing JSON + enrichissement
tickets_df = raw_df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*") \
    .withColumn(
        "equipe_support",
        when(col("type") == "technique", "Equipe Technique")
        .when(col("type") == "administratif", "Service Client")
        .otherwise("Equipe Polyvalente")
    )

#  Affichage dans la console
query = tickets_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Écriture en continu dans un fichier JSON local
query = tickets_df.writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "./export_tickets") \
    .option("checkpointLocation", "./checkpoint_tickets") \
    .start()


query.awaitTermination()
