"""
data_gen.py

Fetches the raw datasets used across the course and saves them to data/.
No filtering or feature engineering happens here; that lives in
preprocessing.py. Every dataset is saved as Parquet, with an optional
CSV backup.

Usage:
    python data_gen.py list
    python data_gen.py fetch --all
    python data_gen.py fetch --name penguins
    python data_gen.py fetch --name nhanes_demo --csv
"""

from pathlib import Path

import pandas as pd
import typer

from core.datasets import REGISTRY, fetch_dataset

app = typer.Typer(help="Fetch raw course datasets into data/.")

DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"


@app.command("list")
def list_datasets() -> None:
    """Print every dataset registered in core/datasets.py."""
    width = max(len(name) for name in REGISTRY)
    for name, spec in REGISTRY.items():
        typer.echo(f"{name:<{width}}  weeks {spec['weeks']}  {spec['description']}")


@app.command("fetch")
def fetch(
    name: str = typer.Option(None, help="Dataset name from `list`."),
    all_datasets: bool = typer.Option(False, "--all", help="Fetch every dataset."),
    csv: bool = typer.Option(False, help="Also write a CSV backup."),
) -> None:
    """Download one or all datasets and save them as Parquet (+ optional CSV)."""
    if not name and not all_datasets:
        raise typer.BadParameter("Pass --name <dataset> or --all.")

    names = list(REGISTRY) if all_datasets else [name]
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for ds in names:
        if ds not in REGISTRY:
            typer.secho(f"Unknown dataset: {ds}", fg="red")
            raise typer.Exit(code=1)

        typer.echo(f"Fetching {ds} ...")
        df: pd.DataFrame = fetch_dataset(ds)

        parquet_path = DATA_DIR / f"{ds}.parquet"
        df.to_parquet(parquet_path, index=False)
        typer.secho(f"  saved {parquet_path} ({len(df):,} rows)", fg="green")

        if csv:
            csv_path = DATA_DIR / f"{ds}.csv"
            df.to_csv(csv_path, index=False)
            typer.secho(f"  saved {csv_path}", fg="green")


if __name__ == "__main__":
    app()
