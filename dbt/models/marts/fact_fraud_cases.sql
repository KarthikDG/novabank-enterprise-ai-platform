{{ config(
    materialized='table'
) }}

with fraud_signals as (

    select *

    from {{ ref('int_fraud_signals') }}

),

customers as (

    select *

    from {{ ref('dim_customer') }}

),

fraud_cases as (

    select

        md5(
            cast(transaction_id as string)
        ) as fraud_case_key,

        transaction_id,

        customer_id,

        transaction_timestamp,

        transaction_amount,

        channel,

        country_code,

        merchant_category,

        fraud_score,

        fraud_risk_level,

        fraud_review_required,

        case

            when fraud_score >= 90
            then 'CRITICAL'

            when fraud_score >= 80
            then 'HIGH'

            when fraud_score >= 40
            then 'MEDIUM'

            else 'LOW'

        end as investigation_priority

    from fraud_signals

),

fraud_enriched as (

    select

        fc.fraud_case_key,

        c.customer_key,

        fc.transaction_id,

        fc.customer_id,

        c.customer_full_name,

        c.customer_segment,

        c.fraud_risk_category,

        fc.transaction_timestamp,

        fc.transaction_amount,

        fc.channel,

        fc.country_code,

        fc.merchant_category,

        fc.fraud_score,

        fc.fraud_risk_level,

        fc.fraud_review_required,

        fc.investigation_priority,

        case

            when fc.fraud_review_required = 'Y'
            then 'OPEN'

            else 'CLOSED'

        end as case_status,

        current_timestamp()
            as case_created_timestamp

    from fraud_cases fc

    left join customers c
        on fc.customer_id = c.customer_id

),

final as (

    select *

    from fraud_enriched

)

select *

from final
