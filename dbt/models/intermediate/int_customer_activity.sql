{{ config(
    materialized='table'
) }}

with customers as (

    select *

    from {{ ref('stg_customer') }}

),

transactions as (

    select *

    from {{ ref('stg_transaction') }}

),

customer_transaction_summary as (

    select

        customer_id,

        count(transaction_id)
            as total_transactions,

        sum(transaction_amount)
            as total_transaction_amount,

        avg(transaction_amount)
            as average_transaction_amount,

        max(transaction_timestamp)
            as last_transaction_timestamp,

        min(transaction_timestamp)
            as first_transaction_timestamp,

        sum(
            case
                when high_value_transaction = 'Y'
                then 1
                else 0
            end
        ) as high_value_transaction_count,

        sum(
            case
                when potential_fraud_flag = 'Y'
                then 1
                else 0
            end
        ) as fraud_signal_count

    from transactions

    group by customer_id

),

customer_channel_summary as (

    select

        customer_id,

        count(
            distinct channel
        ) as unique_channels_used,

        count(
            distinct country_code
        ) as unique_countries_used

    from transactions

    group by customer_id

),

activity_metrics as (

    select

        c.customer_id,

        c.customer_number,

        c.customer_full_name,

        c.country_code,

        c.kyc_status,

        c.risk_rating,

        coalesce(
            s.total_transactions,
            0
        ) as total_transactions,

        coalesce(
            s.total_transaction_amount,
            0
        ) as total_transaction_amount,

        coalesce(
            s.average_transaction_amount,
            0
        ) as average_transaction_amount,

        coalesce(
            s.high_value_transaction_count,
            0
        ) as high_value_transaction_count,

        coalesce(
            s.fraud_signal_count,
            0
        ) as fraud_signal_count,

        coalesce(
            ch.unique_channels_used,
            0
        ) as unique_channels_used,

        coalesce(
            ch.unique_countries_used,
            0
        ) as unique_countries_used,

        s.first_transaction_timestamp,

        s.last_transaction_timestamp

    from customers c

    left join customer_transaction_summary s
        on c.customer_id = s.customer_id

    left join customer_channel_summary ch
        on c.customer_id = ch.customer_id

),

final as (

    select

        customer_id,

        customer_number,

        customer_full_name,

        country_code,

        kyc_status,

        risk_rating,

        total_transactions,

        total_transaction_amount,

        average_transaction_amount,

        high_value_transaction_count,

        fraud_signal_count,

        unique_channels_used,

        unique_countries_used,

        first_transaction_timestamp,

        last_transaction_timestamp,

        case

            when total_transaction_amount >= 100000
            then 'PREMIUM'

            when total_transaction_amount >= 25000
            then 'GOLD'

            else 'STANDARD'

        end as customer_segment,

        current_timestamp()
            as dbt_load_timestamp

    from activity_metrics

)

select *

from final
