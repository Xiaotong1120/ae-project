{{ config(materialized='view') }}

select
  order_id,
  city,
  courier_id,
  aoi_id,
  aoi_type,
  accept_time,
  delivery_time,
  ds
from read_csv_auto(
  '/Users/brandonma/Documents/Study/Projects/ae-project/LaDe_full/delivery/*.csv',
  union_by_name=true
)