import pytest
import pandas as pd
from src.validation import validate_customers, validate_policies

def test_validate_customers_success():
    df = pd.DataFrame({
        "customer_id": ["CUST_001", "CUST_002"],
        "customer_name": ["Alice", "Bob"],
        "date_of_birth": ["1990-01-01", "1985-05-05"],
        "state": ["California", "Texas"]
    })
    assert validate_customers(df) is True

def test_validate_customers_missing_column():
    df = pd.DataFrame({
        "customer_id": ["CUST_001"],
        "customer_name": ["Alice"]
    })
    with pytest.raises(ValueError):
        validate_customers(df)

def test_validate_policies_duplicates():
    df = pd.DataFrame({
        "policy_id": ["POL_001", "POL_001"],
        "customer_id": ["CUST_001", "CUST_002"],
        "vehicle_id": ["VEH_001", "VEH_002"],
        "premium_amount": [500.0, 600.0],
        "policy_status": ["Active", "Expired"]
    })
    with pytest.raises(ValueError):
        validate_policies(df)
