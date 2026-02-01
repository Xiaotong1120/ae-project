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
