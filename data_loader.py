import pandas as pd

def load_data(file_path: str):
    """
    CSV Datei laden, sicherstellen dass 'date' datetime ist.
    """
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    return df
