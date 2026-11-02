{{ config(
    materialized='table'
) }}

with transactions as (

    select *

    from {{ ref('stg_transaction') }}

),

customers as (

    select *

    from {{ ref('dim_customer') }}

),

fraud_signals as (

    select *

    from {{ ref('int_fraud_signals') }}

),

fact_transactions as (

    select

        md5(
            cast(t.transaction_id as string)
        ) as transaction_key,

        c.customer_key,

        t.transaction_id,

        t.customer_id,

        t.account_number,

        t.transaction_amount,

        t.transaction_timestamp,

        cast(
            date(t.transaction_timestamp)
            as date
        ) as transaction_date,

        t.channel,

        t.country_code,

        t.merchant_category,

        t.high_value_transaction,

        t.potential_fraud_flag,

        fs.fraud_score,

        fs.fraud_risk_level,

        fs.fraud_review_required,

        t.transaction_year,

        t.transaction_month,

        t.transaction_day,

        case

            when t.transaction_amount >= 10000
            then 'LARGE'

            when t.transaction_amount >= 1000
            then 'MEDIUM'

            else 'SMALL'

        end as transaction_size_category,

        current_timestamp()
            as fact_load_timestamp

    from transactions t

    left join customers c
        on t.customer_id = c.customer_id

    left join fraud_signals fs
        on t.transaction_id = fs.transaction_id

),

final as (

    select *

    from fact_transactions

)

select *

from final
