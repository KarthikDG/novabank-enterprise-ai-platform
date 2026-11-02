# ============================================================
# NovaBank Audit Framework
# ============================================================

from pyspark.sql import functions as F


class AuditFramework:

    def __init__(self, spark, audit_table):

        self.spark = spark
        self.audit_table = audit_table

    def write_audit_record(
            self,
            pipeline_name,
            layer,
            source_table,
            target_table,
            records_processed,
            status,
            error_message=""
    ):

        audit_df = self.spark.createDataFrame(
            [
                (
                    pipeline_name,
                    layer,
                    source_table,
                    target_table,
                    records_processed,
                    status,
                    error_message
                )
            ],
            [
                "pipeline_name",
                "layer",
                "source_table",
                "target_table",
                "records_processed",
                "status",
                "error_message"
            ]
        ).withColumn(
            "audit_timestamp",
            F.current_timestamp()
        )

        (
            audit_df.write
            .format("delta")
            .mode("append")
            .saveAsTable(
                self.audit_table
            )
        )
