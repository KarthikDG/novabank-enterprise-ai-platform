# ============================================================
# NovaBank Watermark Framework
# ============================================================

from pyspark.sql import functions as F


class WatermarkFramework:

    def __init__(
            self,
            spark,
            watermark_table
    ):

        self.spark = spark
        self.watermark_table = watermark_table

    def get_watermark(
            self,
            pipeline_name
    ):

        result = (
            self.spark.table(
                self.watermark_table
            )
            .filter(
                F.col(
                    "pipeline_name"
                ) == pipeline_name
            )
            .select(
                "watermark_value"
            )
            .first()
        )

        if result:

            return result[0]

        return None

    def update_watermark(
            self,
            pipeline_name,
            watermark_value
    ):

        watermark_df = (
            self.spark.createDataFrame(
                [
                    (
                        pipeline_name,
                        watermark_value
                    )
                ],
                [
                    "pipeline_name",
                    "watermark_value"
                ]
            )
            .withColumn(
                "updated_timestamp",
                F.current_timestamp()
            )
        )

        (
            watermark_df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(
                self.watermark_table
            )
        )
