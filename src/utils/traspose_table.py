import os
import pandas as pd

def trasponseTable(path):
    df = pd.read_csv(path, header=None, encoding="utf-8")
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    df.reset_index(drop=True, inplace=True)
    return df
