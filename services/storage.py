import os
import pandas as pd
from datetime import datetime
from core.models import CDLIntake

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "entries.csv")


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def append_entry(model: CDLIntake) -> None:
    row = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "date": model.date.isoformat(),
        "stream": model.stream,
        "founder_name": model.founder_name,
        "venture_name": model.venture_name,
        "venture_manager_name": model.venture_manager_name,
        "link": str(model.link),
        "comments": model.comments or "",
    }

    df_new = pd.DataFrame([row])

    if os.path.exists(CSV_PATH):
        df_existing = pd.read_csv(CSV_PATH)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(CSV_PATH, index=False)