# ============================================================
# NovaBank Data Quality Framework
# ============================================================

from pyspark.sql import functions as F


class DataQualityFramework:

    @staticmethod
    def check_nulls(
            df,
            column_name
    ):

        return (
            df.filter(
                F.col(column_name).isNull()
            )
            .count()
        )

    @staticmethod
    def check_duplicates(
            df,
            business_key
    ):

        return (
            df.groupBy(business_key)
            .count()
            .filter("count > 1")
            .count()
        )

    @staticmethod
    def check_negative_values(
            df,
            column_name
    ):

        return (
            df.filter(
                F.col(column_name) < 0
            )
            .count()
        )

    @staticmethod
    def validate_required_columns(
            df,
            required_columns
    ):

        missing = list(
            set(required_columns)
            - set(df.columns)
        )

        if missing:

            raise Exception(
                f"""
                Missing Columns:
                {missing}
                """
            )
