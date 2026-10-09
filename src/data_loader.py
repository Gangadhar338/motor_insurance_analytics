import os
import pandas as pd

def check_file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def load_table(file_path: str) -> pd.DataFrame:
    if not check_file_exists(file_path):
        raise FileNotFoundError(f"Required table file not found: {file_path}")
    return pd.read_csv(file_path)

def load_all_data(data_dir: str = "data/raw") -> dict:
    required_files = {"customers": "customers.csv", "vehicles": "vehicles.csv", "policies": "policies.csv", "claims": "claims.csv", "payments": "payments.csv"}
    return {key: load_table(os.path.join(data_dir, filename)) for key, filename in required_files.items()}
