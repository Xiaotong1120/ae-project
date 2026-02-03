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
Delivery duration exhibits a long-tailed distribution, with the majority of orders completed within a few hours.  
A very small number of records contain negative or extremely large durations, which are attributable to inconsistencies or delays in raw event recording rather than metric construction errors.  
These characteristics are explicitly surfaced rather than silently filtered, allowing analytical boundaries to be defined transparently in later stages of the project.  

### Modeling Philosophy
This project prioritizes:   
1. explicit metric definition over implicit calculations,
2. clarity of grain over premature dimensional modeling,
3. and transparency of data limitations over aggressive data filtering.

Dimension tables (e.g. date or location dimensions) are intentionally deferred in this phase, as the project currently focuses on validating and stabilizing a single delivery fact table.
