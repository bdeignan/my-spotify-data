import json
from pathlib import Path

import pandas as pd
from fastcore.utils import *

data_path = Path(__file__).parents[1] / "data"
file_stub = "StreamingHistory"


def read_files(path: Path, file_stub: str = file_stub):
    files = path.glob(file_stub + "*.json")
    data = []

    for file in files:
        with open(file) as f:
            _data = json.load(f)
            print(f"{len(_data)} records, type: {type(_data)}, head: {_data[:2]}")
            data.extend(_data)

    return data


def main():
    global data_path
    global file_stub

    records = read_files(data_path / "raw" / "MyData", file_stub)
    df = pd.DataFrame(records)
    df.columns = [camel2snake(colname) for colname in df.columns]
    print(df.head())

    new_path = data_path / "processed"
    new_path.mkdir(parents=True, exist_ok=True)

    df.to_csv(new_path / "history.csv", index=False)

    print(f'File written: {new_path / "history.csv"}')


if __name__ == "__main__":
    main()
