{{ config(
    materialized='table'
) }}

with customer_activity as (

    select *

    from {{ ref('int_customer_activity') }}

),

customer_dimension as (

    select

        customer_id,

        customer_number,

        customer_full_name,

        country_code,

        kyc_status,

        risk_rating,

        customer_segment,

        total_transactions,

        total_transaction_amount,

        average_transaction_amount,

        fraud_signal_count,

        unique_channels_used,

        unique_countries_used,

        first_transaction_timestamp,

        last_transaction_timestamp,

        case

            when kyc_status = 'APPROVED'
            then 'ACTIVE'

            when kyc_status = 'PENDING'
            then 'REVIEW'

            else 'RESTRICTED'

        end as customer_status,

        case

            when fraud_signal_count >= 10
            then 'HIGH'

            when fraud_signal_count >= 3
            then 'MEDIUM'

            else 'LOW'

        end as fraud_risk_category,

        current_timestamp()
            as dimension_load_timestamp

    from customer_activity

),

final as (

    select

        md5(
            cast(customer_id as string)
        ) as customer_key,

        customer_id,

        customer_number,

        customer_full_name,

        country_code,

        customer_status,

        kyc_status,

        risk_rating,

        customer_segment,

        fraud_risk_category,

        total_transactions,

        total_transaction_amount,

        average_transaction_amount,

        fraud_signal_count,

        unique_channels_used,

        unique_countries_used,

        first_transaction_timestamp,

        last_transaction_timestamp,

        dimension_load_timestamp

    from customer_dimension

)

select *

from final
