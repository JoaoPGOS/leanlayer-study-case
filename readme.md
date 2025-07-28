# Executive Summary

Hi, I’m João Pedro.

This dashboard was built to answer three key questions around forecast accuracy, deal progression, and confidence in next quarter’s pipeline. It’s based on four data sources, merged and cleaned into two main tables: **Deals** and **Pacing**.

The **Deals table** supports the first two questions. By tracking when forecast categories like “Commit” and “Best Case” were assigned, and comparing them to outcomes and stage behavior, I identified **misclassified forecasts** and **stalled deals** — deals stuck too long in a stage.

The **Pacing table** supports the third question. I used weighted forecast values and historical conversion rates per owner to estimate if each is on track, producing a **“Will Hit Target?”** metric with four possible outcomes: Yes, Probably Yes, Probably No, and No.

This setup provides both a retrospective and forward-looking view of performance, helping RevOps make sharper decisions.

---

## 1. “We missed Q1 bookings by 18%. What blew the forecast?”

To answer this, I used the Deals table to compare forecast categories — especially Commit and Best Case — with actual deal outcomes.

The dashboard view shows where these misclassifications are happening by **stage**, and also allows filtering by **owner**.

✅ **Insight:** As you can see most misclassified Commit and Best Case deals came from Prospecting, meaning forecast confidence may have been overestimated at this point in the funnel.

---

## 2. “Where are deals stalling, and why?”

Here, I used the snapshot data to calculate how many days each deal spent in the current stage.

I flagged deals that remained too long — over 30 days — as **stalled**, and grouped them by stage and forecast category.

The view shows both the **volume of stalled deals** and the **average time** in each stage, making it easier to identify bottlenecks.

✅ **Insight:** The biggest slowdown happens in Prospecting — suggesting either re-qualification issues or lack of urgency in moving them forward.

---

## 3. “Given today’s pipe, are we on track for next quarter?”

This is where the Pacing table comes in. I calculated the expected value to close per owner, using forecast weights and historical conversion rates.

I then evaluated if each owner has enough pipeline, time, and pacing to hit their target — resulting in the **“Will Hit Target?”** metric: Yes, Probably Yes, Probably No, or No.

The dashboard gives a clear breakdown by **owner**, combining open deals, estimated value and expected pace.

✅ **Insight:** While some owners are on track, others show gaps in either open pipeline or pace — giving leadership a chance to act now before the quarter ends.


# ETL Process Documentation

This notebook performs an ETL (Extract, Transform, Load) process structured as follows:

## 1. Importing necessary libraries
The first step involves importing essential Python libraries, primarily `pandas`, which is used for handling and manipulating data in tabular form. These imports ensure that all required functions and tools are available for the rest of the notebook.

## 2. Loading data from external sources
Data is read from one or more external sources such as CSV, Excel, or other file formats. The data is loaded into DataFrames, allowing for further manipulation using the pandas library.

## 3. Performing data transformations
After loading, various transformations are applied to the datasets. These can include creating new calculated columns, converting data types, filtering rows, or formatting string and date values to ensure consistency and usability.

## 4. Aggregating or grouping data
The data is then grouped by one or more columns to summarize it, usually using aggregation functions such as sum, mean, or count. This step is crucial for consolidating the data into a more usable format, especially when preparing for reporting or analysis.

## 5. Merging or joining datasets
Multiple DataFrames are combined through merge or join operations, typically using a common key. This integrates information from different sources into a single, cohesive dataset.

## 6. Exporting processed data
Once the data has been cleaned, transformed, and merged, it is saved to a new file—such as a CSV or Excel spreadsheet—for storage, sharing, or input into another system or tool.

