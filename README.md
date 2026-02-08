## ae-project

This project focuses on transforming raw delivery task events into an analytics-ready delivery fact table with a clearly defined grain and duration logic, enabling consistent bottleneck analysis across multiple spatial and operational dimensions.

### Business Question
How can analytics-ready delivery data be used to identify bottlenecks across different areas of interest (AOIs) in the last-mile delivery process?

### Dataset Description
This project uses a subset of the LaDe (Last-mile Delivery) public dataset, focusing on delivery-stage operational data for on-demand orders.
Each row represents a single delivery task, capturing the period from task acceptance to delivery completion, along with key spatial and contextual attributes such as city, area of interest (AOI), and courier.

### Grain
One row per order per delivery task, representing the delivery phase from task acceptance to delivery completion.

### Core Analysis Goal
Using this dataset, the goal of this project is to analyze whether deliveries to different Areas of Interest (AOIs) are systematically slower during the delivery phase.

### Metric Definition and Data Validation Notes

Delivery duration is derived as the time difference between task acceptance and delivery completion timestamps.  
During metric construction, the following characteristics of the raw data were observed:  
1. Delivery duration exhibits a long-tailed distribution, with the majority of orders completed within a few hours.  
2. A very small number of records contain negative or extremely large durations, which are attributable to inconsistencies or delays in raw event recording rather than metric construction errors.  
3. These characteristics are explicitly surfaced rather than silently filtered, allowing analytical boundaries to be defined transparently in later stages of the project.  

#### Fact Table: fact_delivery
fact_delivery is an analytics-ready delivery fact table derived from raw LaDe delivery-stage task data.  
Grain: one row per order per delivery task
1. Core fields: order_id, accept_time, delivery_time, city, aoi_id, aoi_type, courier_id, ds
2. Derived metric: delivery_duration_minutes
3. Analysis flags: is_valid_for_bottleneck, delivery_duration_category  
The goal is to standardize delivery-stage performance at a consistent grain, enabling reusable bottleneck analysis across AOI and other operational dimensions.

### Delivery Duration Analysis Boundary
Exploratory validation of the delivery duration metric shows that the majority of delivery tasks follow a consistent operational pattern, while a small fraction exhibit fundamentally different completion behavior.   
   
Specifically:
1. Approximately 95% of deliveries are completed within 8 hours.
2. Around 99% of deliveries are completed within 24 hours.
3. Beyond the 24-hour mark, delivery duration enters a distinct long-tail regime, with sharply reduced density and significantly different completion dynamics.
  
This distributional break indicates a transition from standard delivery execution to exceptional or delayed completion scenarios (e.g. postponed confirmation, multi-day holding, or late event recording).  
For this reason, AOI-level bottleneck analysis in this project focuses on deliveries completed within a 24-hour window.  
Rather than removing long-tail records, the model explicitly flags which deliveries are suitable for bottleneck analysis, preserving transparency and analytical flexibility.  

### Modeling Philosophy
This project prioritizes:   
1. explicit metric definition over implicit calculations,
2. clarity of grain over premature dimensional modeling,
3. and transparency of data limitations over aggressive data filtering.

Dimension tables (e.g. date or location dimensions) are intentionally deferred in this phase, as the project currently focuses on validating and stabilizing a single delivery fact table.
