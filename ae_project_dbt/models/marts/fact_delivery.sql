{{ config(materialized='table') }}

with source as (
    select *
    from {{ ref('stg_lade_delivery') }}
),

typed as (
    select
        order_id,
        city,
        aoi_id,
        aoi_type,
        courier_id,
        ds,

        -- raw time strings: 'MM-DD HH:MM:SS' (no year)
        cast('2022-' || accept_time as timestamp)   as accept_time,
        cast('2022-' || delivery_time as timestamp) as delivery_time
    from source
),

metrics as (
    select
        *,
        datediff('minute', accept_time, delivery_time) as delivery_duration_minutes
    from typed
),

flags as (
    select
        *,
        case
            when delivery_duration_minutes < 0 then false
            when delivery_duration_minutes <= 1440 then true
            else false
        end as is_valid_for_bottleneck,

        case
            when delivery_duration_minutes < 0 then 'invalid'
            when delivery_duration_minutes <= 1440 then 'standard_delivery'
            else 'long_tail_delivery'
        end as delivery_duration_category
    from metrics
)

select * from flags