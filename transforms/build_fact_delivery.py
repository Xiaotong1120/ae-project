"""
This module builds the analytics-ready fact_delivery table
from raw LaDe delivery-stage data.

Key modeling choices:
- One row per order per delivery task
- Delivery duration is derived from accept_time and delivery_time
- A delivery is considered valid for AOI bottleneck analysis
  if it completes within 24 hours (1440 minutes)
- Long-tail deliveries are retained but explicitly flagged
"""

import pandas as pd

def load_and_combine_delivery_data(file_paths: list[str]) -> pd.DataFrame:
    """
    Load and combine multiple city-level delivery CSV files.
    """
    dfs = [pd.read_csv(path) for path in file_paths]
    return pd.concat(dfs, ignore_index=True)

def parse_delivery_timestamps(
    df: pd.DataFrame,
    year: int = 2022
) -> pd.DataFrame:
    """
    Parse accept_time and delivery_time into datetime.
    Assumes timestamps are in MM-DD HH:MM:SS format.
    """
    df = df.copy()

    df["accept_time"] = pd.to_datetime(
        df["accept_time"].apply(lambda x: f"{year}-{x}"),
        errors="coerce"
    )

    df["delivery_time"] = pd.to_datetime(
        df["delivery_time"].apply(lambda x: f"{year}-{x}"),
        errors="coerce"
    )

    return df

def add_delivery_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive delivery_duration_minutes from timestamps.
    """
    df = df.copy()

    df["delivery_duration_minutes"] = (
        (df["delivery_time"] - df["accept_time"])
        .dt.total_seconds()
        .div(60)
    )

    return df

def add_bottleneck_flags(
    df: pd.DataFrame,
    max_minutes: int = 1440
) -> pd.DataFrame:
    """
    Explicitly flag whether a delivery record is valid
    for AOI bottleneck analysis.
    """
    df = df.copy()

    df["is_valid_for_bottleneck"] = (
        (df["delivery_duration_minutes"] >= 0) &
        (df["delivery_duration_minutes"] <= max_minutes)
    )

    def categorize_duration(x):
        if x < 0:
            return "invalid"
        elif x <= max_minutes:
            return "standard_delivery"
        else:
            return "long_tail_delivery"

    df["delivery_duration_category"] = (
        df["delivery_duration_minutes"]
        .apply(categorize_duration)
    )

    return df

def build_fact_delivery(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Build the analytics-ready fact_delivery table.
    """
    df = df_raw.copy()

    fact_columns = [
        "order_id",
        "accept_time",
        "delivery_time",
        "delivery_duration_minutes",
        "city",
        "aoi_id",
        "aoi_type",
        "courier_id",
        "ds",
        "is_valid_for_bottleneck",
        "delivery_duration_category",
    ]

    return df[fact_columns]

if __name__ == "__main__":
    delivery_files = [
        "LaDe_full/delivery/delivery_hz.csv",
        "LaDe_full/delivery/delivery_cq.csv",
        "LaDe_full/delivery/delivery_jl.csv",
        "LaDe_full/delivery/delivery_sh.csv",
        "LaDe_full/delivery/delivery_yt.csv",
    ]

    df_raw = load_and_combine_delivery_data(delivery_files)
    df_raw = parse_delivery_timestamps(df_raw)
    df_raw = add_delivery_duration(df_raw)
    df_raw = add_bottleneck_flags(df_raw)

    fact_delivery = build_fact_delivery(df_raw)

    print(fact_delivery.head())