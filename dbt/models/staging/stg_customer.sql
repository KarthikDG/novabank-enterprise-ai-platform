{{ config(
    materialized='view'
) }}

with source_customer as (

    select *

    from {{ source(
        'customer',
        'customer_silver'
    ) }}

),

standardized_customer as (

    select

        cast(CustomerID as bigint)
            as customer_id,

        cast(CustomerNumber as string)
            as customer_number,

        trim(upper(FirstName))
            as first_name,

        trim(upper(LastName))
            as last_name,

        trim(lower(EmailAddress))
            as email_address,

        trim(upper(CountryCode))
            as country_code,

        cast(DateOfBirth as date)
            as date_of_birth,

        trim(upper(KYCStatus))
            as kyc_status,

        trim(upper(RiskRating))
            as risk_rating,

        cast(ValidEmail as string)
            as valid_email,

        cast(CustomerFullName as string)
            as customer_full_name,

        cast(RecordSource as string)
            as record_source,

        cast(SilverLoadTimestamp as timestamp)
            as silver_load_timestamp

    from source_customer

),

final as (

    select

        customer_id,
        customer_number,
        first_name,
        last_name,
        customer_full_name,
        email_address,
        country_code,
        date_of_birth,
        kyc_status,
        risk_rating,
        valid_email,
        record_source,
        silver_load_timestamp,

        current_timestamp()
            as dbt_load_timestamp

    from standardized_customer

)

select *

from final
