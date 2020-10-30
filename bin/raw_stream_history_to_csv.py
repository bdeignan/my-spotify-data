import json
from pathlib import Path

import pandas as pd
from fastcore.utils import *

DATA_PATH = Path(__file__).parents[1] / 'data' 
FILE_STUB = 'StreamingHistory'

def read_files(path: Path, file_stub: str=FILE_STUB):
    files = path.glob(file_stub + '*.json')
    data = []

    for file in files:
        with open(file) as f:
            _data = json.load(f)
            print(f'{len(_data)} records, type: {type(_data)}, head: {_data[:2]}')
            data.extend(_data)

    return data

def main():
    global DATA_PATH
    global FILE_STUB

    records = read_files(DATA_PATH / 'raw' / 'MyData', FILE_STUB)
    df = pd.DataFrame(records)
    df.columns = [camel2snake(colname) for colname in df.columns]
    print(df.head())

    new_path = DATA_PATH / 'processed'
    new_path.mkdir(parents=True, exist_ok=True)

    df.to_csv(new_path / 'history.csv', index=False)

    print(f'File written: {new_path / "history.csv"}')

if __name__ == '__main__':
    main()