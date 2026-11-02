{{ config(
    materialized='table'
) }}

with transactions as (

    select *

    from {{ ref('stg_transaction') }}

),

customer_activity as (

    select *

    from {{ ref('int_customer_activity') }}

),

fraud_rules as (

    select

        t.transaction_id,

        t.customer_id,

        t.transaction_amount,

        t.transaction_timestamp,

        t.channel,

        t.country_code,

        t.merchant_category,

        t.high_value_transaction,

        t.potential_fraud_flag,

        ca.total_transactions,

        ca.total_transaction_amount,

        ca.fraud_signal_count,

        case
            when t.transaction_amount >= 10000
            then 40
            else 0
        end as amount_risk_score,

        case
            when t.high_value_transaction = 'Y'
            then 20
            else 0
        end as high_value_risk_score,

        case
            when t.potential_fraud_flag = 'Y'
            then 30
            else 0
        end as fraud_flag_risk_score,

        case
            when ca.fraud_signal_count >= 5
            then 10
            else 0
        end as customer_history_risk_score

    from transactions t

    left join customer_activity ca
        on t.customer_id = ca.customer_id

),

fraud_scoring as (

    select

        *,

        (
            amount_risk_score
            + high_value_risk_score
            + fraud_flag_risk_score
            + customer_history_risk_score
        ) as fraud_score

    from fraud_rules

),

risk_classification as (

    select

        *,

        case

            when fraud_score >= 80
            then 'HIGH'

            when fraud_score >= 40
            then 'MEDIUM'

            else 'LOW'

        end as fraud_risk_level,

        case

            when fraud_score >= 80
            then 'Y'

            else 'N'

        end as fraud_review_required

    from fraud_scoring

),

final as (

    select

        transaction_id,

        customer_id,

        transaction_amount,

        transaction_timestamp,

        channel,

        country_code,

        merchant_category,

        total_transactions,

        total_transaction_amount,

        fraud_signal_count,

        fraud_score,

        fraud_risk_level,

        fraud_review_required,

        current_timestamp()
            as dbt_load_timestamp

    from risk_classification

)

select *

from final
