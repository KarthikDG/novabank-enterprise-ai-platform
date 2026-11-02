{{ config(
    materialized='view'
) }}

with source_transactions as (

    select *

    from {{ source(
        'transactions',
        'transactions_silver'
    ) }}

),

standardized_transactions as (

    select

        cast(TransactionID as bigint)
            as transaction_id,

        cast(CustomerID as bigint)
            as customer_id,

        cast(AccountNumber as string)
            as account_number,

        cast(TransactionAmount as decimal(18,2))
            as transaction_amount,

        cast(TransactionDate as timestamp)
            as transaction_timestamp,

        trim(upper(Channel))
            as channel,

        trim(upper(CountryCode))
            as country_code,

        trim(upper(MerchantCategory))
            as merchant_category,

        cast(HighValueTransaction as string)
            as high_value_transaction,

        cast(PotentialFraudFlag as string)
            as potential_fraud_flag,

        cast(TransactionYear as integer)
            as transaction_year,

        cast(TransactionMonth as integer)
            as transaction_month,

        cast(TransactionDay as integer)
            as transaction_day,

        cast(SilverLoadTimestamp as timestamp)
            as silver_load_timestamp

    from source_transactions

),

final as (

    select

        transaction_id,

        customer_id,

        account_number,

        transaction_amount,

        transaction_timestamp,

        channel,

        country_code,

        merchant_category,

        high_value_transaction,

        potential_fraud_flag,

        transaction_year,

        transaction_month,

        transaction_day,

        silver_load_timestamp,

        current_timestamp()
            as dbt_load_timestamp

    from standardized_transactions

)

select *

from final
