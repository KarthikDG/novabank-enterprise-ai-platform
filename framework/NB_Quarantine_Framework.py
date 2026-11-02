# ============================================================
# NovaBank Quarantine Framework
# ============================================================

from pyspark.sql import functions as F


class QuarantineFramework:

    def __init__(
            self,
            quarantine_table
    ):

        self.quarantine_table = quarantine_table

    def quarantine_records(
            self,
            dataframe,
            quarantine_reason
    ):

        quarantine_df = (
            dataframe
            .withColumn(
                "quarantine_reason",
                F.lit(
                    quarantine_reason
                )
            )
            .withColumn(
                "quarantine_timestamp",
                F.current_timestamp()
            )
        )

        (
            quarantine_df.write
            .format("delta")
            .mode("append")
            .saveAsTable(
                self.quarantine_table
            )
        )

    def filter_valid_records(
            self,
            dataframe,
            filter_condition
    ):

        valid_records = (
            dataframe
            .filter(filter_condition)
        )

        invalid_records = (
            dataframe
            .filter(
                ~filter_condition
            )
        )

        return (
            valid_records,
            invalid_records
        )
