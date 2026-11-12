"""
preprocessing.py

Cleaning and feature engineering for course datasets. Reads raw Parquet
from data/raw/ and writes cleaned Parquet to data/processed/. Each week
that needs a cleaned table gets its own function here so students can
read exactly what was done to the data.

Usage:
    python preprocessing.py
"""

from pathlib import Path

import pandas as pd

from core.datasets import load_raw

PROCESSED_DIR = Path(__file__).resolve().parent / "data" / "processed"


def build_nhanes() -> pd.DataFrame:
    """Week 2 / 7 / 8: merge the four NHANES components on SEQN, keep a
    small analysis set, and recode the diabetes question to 0/1."""
    demo = load_raw("nhanes_demo")[
        ["SEQN", "RIAGENDR", "RIDAGEYR", "RIDRETH3", "INDFMPIR", "WTMEC2YR"]
    ]
    bmx = load_raw("nhanes_bmx")[["SEQN", "BMXWT", "BMXHT", "BMXBMI", "BMXWAIST"]]
    bpx = load_raw("nhanes_bpx")[["SEQN", "BPXSY1", "BPXDI1"]]
    diq = load_raw("nhanes_diq")[["SEQN", "DIQ010"]]

    df = demo.merge(bmx, on="SEQN", how="left").merge(bpx, on="SEQN", how="left")
    df = df.merge(diq, on="SEQN", how="inner")  # questionnaire defines the cohort

    # DIQ010: 1 = yes, 2 = no, 3 = borderline, 7 = refused, 9 = don't know
    df = df[df["DIQ010"].isin([1, 2, 3])].copy()
    df["diabetes"] = (df["DIQ010"] == 1).astype(int)

    df = df.rename(columns={
        "RIAGENDR": "sex", "RIDAGEYR": "age", "RIDRETH3": "race_eth",
        "INDFMPIR": "income_ratio", "WTMEC2YR": "weight_mec",
        "BMXWT": "weight_kg", "BMXHT": "height_cm", "BMXBMI": "bmi",
        "BMXWAIST": "waist_cm", "BPXSY1": "sbp", "BPXDI1": "dbp",
    })
    return df.drop(columns="DIQ010")


def clean_adult(df: pd.DataFrame) -> pd.DataFrame:
    """Week 7 / 8 / 13: binary target, trimmed strings."""
    out = df.copy()
    out["income"] = (out["income"].str.strip() == ">50K").astype(int)
    return out


BUILDERS = {
    "nhanes": build_nhanes,
    "adult": lambda: clean_adult(load_raw("adult")),
}


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name, fn in BUILDERS.items():
        df = fn()
        path = PROCESSED_DIR / f"{name}.parquet"
        df.to_parquet(path, index=False)
        print(f"wrote {path} ({len(df):,} rows)")


if __name__ == "__main__":
    main()
