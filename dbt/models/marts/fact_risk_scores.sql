{{ config(
    materialized='table'
) }}

with customers as (

    select *

    from {{ ref('dim_customer') }}

),

transactions as (

    select *

    from {{ ref('fact_transactions') }}

),

customer_risk_metrics as (

    select

        customer_id,

        count(transaction_id)
            as transaction_count,

        sum(transaction_amount)
            as total_exposure,

        avg(transaction_amount)
            as average_transaction_amount,

        max(transaction_amount)
            as maximum_transaction_amount,

        sum(
            case
                when fraud_risk_level = 'HIGH'
                then 1
                else 0
            end
        ) as high_risk_transaction_count

    from transactions

    group by customer_id

),

risk_scoring as (

    select

        c.customer_key,

        c.customer_id,

        c.customer_number,

        c.customer_full_name,

        c.customer_segment,

        c.risk_rating,

        c.fraud_risk_category,

        crm.transaction_count,

        crm.total_exposure,

        crm.average_transaction_amount,

        crm.maximum_transaction_amount,

        crm.high_risk_transaction_count,

        case

            when crm.total_exposure >= 500000
            then 50

            when crm.total_exposure >= 100000
            then 30

            else 10

        end as exposure_score,

        case

            when crm.high_risk_transaction_count >= 10
            then 30

            when crm.high_risk_transaction_count >= 3
            then 15

            else 5

        end as fraud_score_component,

        case

            when c.customer_segment = 'PREMIUM'
            then 20

            when c.customer_segment = 'GOLD'
            then 15

            else 10

        end as segment_score

    from customers c

    left join customer_risk_metrics crm
        on c.customer_id = crm.customer_id

),

final_risk_score as (

    select

        *,

        (
            exposure_score
            + fraud_score_component
            + segment_score
        ) as enterprise_risk_score

    from risk_scoring

),

risk_classification as (

    select

        *,

        case

            when enterprise_risk_score >= 80
            then 'HIGH'

            when enterprise_risk_score >= 50
            then 'MEDIUM'

            else 'LOW'

        end as enterprise_risk_level

    from final_risk_score

),

final as (

    select

        md5(
            cast(customer_id as string)
        ) as risk_record_key,

        customer_key,

        customer_id,

        customer_number,

        customer_full_name,

        customer_segment,

        risk_rating,

        fraud_risk_category,

        transaction_count,

        total_exposure,

        average_transaction_amount,

        maximum_transaction_amount,

        high_risk_transaction_count,

        enterprise_risk_score,

        enterprise_risk_level,

        current_timestamp()
            as risk_calculation_timestamp

    from risk_classification

)

select *

from final
