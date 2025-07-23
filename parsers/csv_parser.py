# This parser helps us turn CSV files into readable text tables.
import pandas as pd

def parse_csv(file_path):
    """
    Reads a CSV file and returns its contents as a nicely formatted string (like a table).
    """
    df = pd.read_csv(file_path)
    return df.to_string(index=False)
