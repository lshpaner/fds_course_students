"""
core/datasets.py

Registry of raw course datasets and a single fetch function.
Each entry records where the data comes from, which weeks use it,
and a loader that returns a raw pandas DataFrame. Nothing is cleaned
here; that is preprocessing.py's job.
"""

from typing import Callable

import pandas as pd

SEABORN_RAW = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/{name}.csv"
UCI = "https://archive.ics.uci.edu/ml/machine-learning-databases/{path}"

ADULT_COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country",
    "income",
]

WINE_COLUMNS = [
    "cultivar", "alcohol", "malic_acid", "ash", "alcalinity_of_ash",
    "magnesium", "total_phenols", "flavanoids", "nonflavanoid_phenols",
    "proanthocyanins", "color_intensity", "hue", "od280_od315",
    "proline",
]


NHANES_XPT = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/{file}.xpt"


def _nhanes(file: str) -> Callable[[], pd.DataFrame]:
    """NHANES 2017-2018 component file (SAS transport format)."""
    def loader() -> pd.DataFrame:
        df = pd.read_sas(NHANES_XPT.format(file=file), format="xport")
        df["SEQN"] = df["SEQN"].astype(int)  # participant id, the join key
        return df
    return loader


def _seaborn(name: str) -> Callable[[], pd.DataFrame]:
    return lambda: pd.read_csv(SEABORN_RAW.format(name=name))


def _adult() -> pd.DataFrame:
    return pd.read_csv(
        UCI.format(path="adult/adult.data"),
        header=None,
        names=ADULT_COLUMNS,
        skipinitialspace=True,
        na_values="?",
    )


def _wine() -> pd.DataFrame:
    return pd.read_csv(
        UCI.format(path="wine/wine.data"), header=None, names=WINE_COLUMNS
    )


def _newsgroups() -> pd.DataFrame:
    # Text corpus for the language-models week. Four categories keep it small.
    from sklearn.datasets import fetch_20newsgroups

    cats = ["sci.med", "sci.space", "rec.sport.baseball", "talk.politics.misc"]
    bunch = fetch_20newsgroups(
        subset="all", categories=cats, remove=("headers", "footers", "quotes")
    )
    return pd.DataFrame(
        {"text": bunch.data, "target": bunch.target,
         "category": [bunch.target_names[t] for t in bunch.target]}
    )


def _fluview() -> pd.DataFrame:
    # National weekly influenza-like illness from CDC FluView, served by the CMU Delphi Epidata API.
    import json
    from urllib.request import urlopen

    url = "https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=201001-202552"
    with urlopen(url, timeout=60) as r:
        payload = json.load(r)
    df = pd.DataFrame(payload["epidata"])
    return df[["epiweek", "wili", "ili", "num_ili", "num_patients", "num_providers"]]


def _hospital_contacts() -> pd.DataFrame:
    # SocioPatterns hospital ward contact network (Lyon, 2010): face-to-face contacts between patients and staff,
    # 20-second resolution over ~5 days. Mirrored by Netzschleuder (networks.skewed.de) as a CSV bundle.
    # Output columns: t (seconds), i, j (person ids), role_i, role_j (PAT, NUR, MED, ADM).
    import io
    import zipfile
    from urllib.request import Request, urlopen

    url = "https://networks.skewed.de/net/sp_hospital/files/sp_hospital.csv.zip"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as r:
        z = zipfile.ZipFile(io.BytesIO(r.read()))

    def read(name: str) -> pd.DataFrame:
        df = pd.read_csv(z.open(name))
        df.columns = [c.strip().lstrip("#").strip() for c in df.columns]
        return df

    nodes = read("nodes.csv")
    edges = read("edges.csv")
    role = nodes.set_index(nodes.columns[0])["status"]   # first column is the node index used in edges.csv
    out = pd.DataFrame({
        "t": edges["time"].astype(int),
        "i": edges["source"].astype(int),
        "j": edges["target"].astype(int),
    })
    out["role_i"] = out["i"].map(role)
    out["role_j"] = out["j"].map(role)
    return out.sort_values("t").reset_index(drop=True)


REGISTRY: dict[str, dict] = {
    "penguins": {
        "loader": _seaborn("penguins"),
        "weeks": [1, 4, 9],
        "description": "Palmer penguins; small, clean-ish, good first dataset.",
    },
    "nhanes_demo": {
        "loader": _nhanes("DEMO_J"),
        "weeks": [2, 7, 8],
        "description": "NHANES 2017-18 demographics (age, sex, race, income, survey weights).",
    },
    "nhanes_bmx": {
        "loader": _nhanes("BMX_J"),
        "weeks": [2, 7, 8],
        "description": "NHANES 2017-18 body measures (weight, height, BMI, waist).",
    },
    "nhanes_bpx": {
        "loader": _nhanes("BPX_J"),
        "weeks": [2, 7, 8],
        "description": "NHANES 2017-18 blood pressure exam readings.",
    },
    "nhanes_diq": {
        "loader": _nhanes("DIQ_J"),
        "weeks": [2, 7, 8],
        "description": "NHANES 2017-18 diabetes questionnaire (classification target).",
    },
    "nhanes_smq": {
        "loader": _nhanes("SMQ_J"),
        "weeks": [2],
        "description": "NHANES 2017-18 smoking questionnaire (HW1; skip patterns).",
    },
    "nhanes_bpq": {
        "loader": _nhanes("BPQ_J"),
        "weeks": [2],
        "description": "NHANES 2017-18 blood pressure / cholesterol questionnaire (HW1).",
    },
    "nhanes_ghb": {
        "loader": _nhanes("GHB_J"),
        "weeks": [13],
        "description": "NHANES 2017-18 glycohemoglobin (HbA1c) lab values (HW7; lab-measured diabetes label).",
    },
    "fluview": {
        "loader": _fluview,
        "weeks": [10],
        "description": "CDC FluView national weekly ILI, 2010-2025, via CMU Delphi Epidata (time series).",
    },
    "hospital_contacts": {
        "loader": _hospital_contacts,
        "weeks": [11],
        "description": "SocioPatterns hospital ward face-to-face contacts (75 people, 5 days); network analysis.",
    },
    "tips": {
        "loader": _seaborn("tips"),
        "weeks": [3, 5],
        "description": "Restaurant tips; statistics recap and visualization.",
    },
    "diamonds": {
        "loader": _seaborn("diamonds"),
        "weeks": [6],
        "description": "Diamond prices; regression with mixed feature types.",
    },
    "flights": {
        "loader": _seaborn("flights"),
        "weeks": [10],
        "description": "Monthly airline passengers 1949-1960; time series.",
    },
    "adult": {
        "loader": _adult,
        "weeks": [7, 8, 13],
        "description": "UCI Adult income; classification, evaluation, fairness.",
    },
    "wine": {
        "loader": _wine,
        "weeks": [9],
        "description": "UCI Wine chemistry; clustering and PCA.",
    },
    "newsgroups": {
        "loader": _newsgroups,
        "weeks": [12],
        "description": "20 Newsgroups subset; embeddings and language models.",
    },
}


def fetch_dataset(name: str) -> pd.DataFrame:
    """Return the raw DataFrame for a registered dataset."""
    return REGISTRY[name]["loader"]()


def load_raw(name: str, data_dir: str = "data/raw") -> pd.DataFrame:
    """Read a previously fetched raw Parquet file (used inside notebooks)."""
    return pd.read_parquet(f"{data_dir}/{name}.parquet")