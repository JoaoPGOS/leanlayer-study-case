# Important Links

### [Loom](https://www.loom.com/share/b406a7a6591a4fc38587a5333d902d39?sid=96805534-08f1-4187-af51-b73dd597cd43)
### [Looker Dashboard](https://lookerstudio.google.com/u/0/reporting/a936de49-1efb-45dd-b62f-e93ceada830d/page/5jiSF)

# Executive Summary

Hi, I’m João Pedro.

This dashboard was built to answer three key questions around forecast accuracy, deal progression, and confidence in next quarter’s pipeline. It’s based on four data sources, merged and cleaned into two main tables: **Deals** and **Pacing**.

The **Deals table** supports the first two questions. By tracking when forecast categories like “Commit” and “Best Case” were assigned, and comparing them to outcomes and stage behavior, I identified **misclassified forecasts** and **stalled deals** — deals stuck too long in a stage.

The **Pacing table** supports the third question. I used weighted forecast values and historical conversion rates per owner to estimate if each is on track, producing a **“Will Hit Target?”** metric with four possible outcomes: Yes, Probably Yes, Probably No, and No.

This setup provides both a retrospective and forward-looking view of performance, helping RevOps make sharper decisions.

---

## 1. “We missed Q1 bookings by 18%. What blew the forecast?”

The analysis reveals that optimism was concentrated too early in the funnel. Many deals tagged as "Commit" or "Best Case" ultimately didn’t close — particularly those still in early stages like Prospecting. This points to a **systematic overconfidence in immature opportunities**, suggesting that forecast discipline needs to improve at the top of the pipeline.

✅ **Insight:** Forecast accuracy broke down not due to last-minute slippage, but because of early-stage deals being treated as highly probable too soon. Improving qualification and stricter forecast gating criteria at these stages could significantly boost reliability.

---

## 2. “Where are deals stalling, and why?”

The pipeline is losing momentum in early stages — especially Prospecting — where deals tend to remain idle far too long. This suggests **front-of-funnel inefficiency**, likely caused by poor qualification or misalignment between sales activity and opportunity readiness.

✅ **Insight:** Most pipeline friction isn’t happening late in the cycle — it’s happening right at the start. This slows velocity and clogs the funnel. Better qualification criteria and clearer ownership at early stages could help unblock the flow.

---

## 3. “Given today’s pipe, are we on track for next quarter?”

Looking forward, the picture is mixed. While some reps are well-positioned, others face real risk. Gaps in pipeline value, pacing, or remaining time mean several contributors are **unlikely to reach their goals without intervention**.

✅ **Insight:** There’s still time to act — but only if action is targeted. The pacing analysis gives clear visibility into which owners need more deals, faster movement, or both. This enables focused support and prioritization before it’s too late.

----

# ETL Process Documentation

This notebook performs an ETL (Extract, Transform, Load) pipeline focused on sales and pipeline data, particularly combining pacing, full deals, and forecast information. Below is a breakdown of the key stages with real examples from the notebook.

---

## 1. Importing Necessary Libraries

The script starts by importing essential Python libraries such as:

```python
import pandas as pd
import numpy as np
```

These are used for data manipulation, cleaning, and analysis throughout the notebook.

---

## 2. Loading Data from External Sources

Data is read from multiple CSV files, each representing a key dataset used in the analysis:

```python
pacing_df = pd.read_csv("data/01_raw/pacing.csv")
full_deals_df = pd.read_csv("data/01_raw/full_deals.csv")
forecast_df = pd.read_csv("data/01_raw/forecast.csv")
```

Each of these files corresponds to a business process component (e.g., actual deals, projected pipeline, sales forecast).

---

## 3. Performing Data Transformations

Several transformations are applied to clean and prepare the data. Key steps include:

- **Date conversion**:
  ```python
  pacing_df["date"] = pd.to_datetime(pacing_df["date"])
  ```

- **Adding derived columns to `pacing_df`**:
  ```python
  pacing_df["gap"] = pacing_df["target_amount"] - pacing_df["estimated_value"]
  pacing_df["pacing"] = pacing_df["estimated_value"] / pacing_df["target_amount"]
  ```

- **Merging owners into deals**:
  ```python
  full_deals_df = full_deals_df.merge(
      pacing_df[["owner_id", "name"]],
      on="owner_id",
      how="left"
  )
  ```

- **Rounding values for consistency**:
  ```python
  pacing_df[["estimated_value", "gap", "target_amount"]] = pacing_df[["estimated_value", "gap", "target_amount"]].round(0).astype(float)
  pacing_df["pacing"] = pacing_df["pacing"].round(2).astype(float)
  ```

---

## 4. Aggregating or Grouping Data

Although not heavily used in the visible cells, aggregations like `.groupby()` and `.sum()` or `.mean()` are often used to consolidate pacing or forecast values by month, team, or owner.

---

## 5. Merging or Joining Datasets

Multiple datasets are joined to enrich the final view:

- **Deal owners merged into `full_deals_df`**:
  ```python
  full_deals_df = full_deals_df.merge(
      pacing_df[["owner_id", "name"]],
      on="owner_id",
      how="left"
  )
  ```

- Additional merges may happen in later stages when `forecast_df` is aligned with the other datasets.

---

## 6. Exporting Processed Data

The processed data is then exported back into files for further use in reporting or dashboard tools:

```python
pacing_df.to_csv("data/02_clean/pacing_clean.csv", index=False)
full_deals_df.to_csv("data/02_clean/full_deals_enriched.csv", index=False)
```

---

## Notes

- The ETL pipeline is designed for integration with Looker or other BI tools.
- Data sources are organized by raw and clean folders (`data/01_raw/` and `data/02_clean/`).
- No database or API connections are involved; the data is handled locally through CSVs.

