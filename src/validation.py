import pandas as pd

def validate_customers(df: pd.DataFrame) -> bool:
    required = ["customer_id", "customer_name", "date_of_birth", "state"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column in customers: {col}")
    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer_id found in customers table.")
    return True

def validate_vehicles(df: pd.DataFrame) -> bool:
    required = ["vehicle_id", "customer_id", "vehicle_type", "vehicle_year"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column in vehicles: {col}")
    if df["vehicle_id"].duplicated().any():
        raise ValueError("Duplicate vehicle_id found in vehicles table.")
    return True

def validate_policies(df: pd.DataFrame) -> bool:
    required = ["policy_id", "customer_id", "vehicle_id", "premium_amount", "policy_status"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column in policies: {col}")
    if df["policy_id"].duplicated().any():
        raise ValueError("Duplicate policy_id found in policies table.")
    return True

def validate_claims(df: pd.DataFrame) -> bool:
    required = ["claim_id", "policy_id", "customer_id", "claim_amount", "claim_status"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column in claims: {col}")
    if df["claim_id"].duplicated().any():
        raise ValueError("Duplicate claim_id found in claims table.")
    return True

def validate_payments(df: pd.DataFrame) -> bool:
    required = ["payment_id", "claim_id", "policy_id", "payment_amount"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column in payments: {col}")
    if df["payment_id"].duplicated().any():
        raise ValueError("Duplicate payment_id found in payments table.")
    return True

def validate_relationships(data: dict) -> bool:
    customers, vehicles, policies, claims, payments = data["customers"], data["vehicles"], data["policies"], data["claims"], data["payments"]
    if not vehicles["customer_id"].isin(customers["customer_id"]).all():
        raise ValueError("Orphaned customer_id found in vehicles table.")
    if not policies["customer_id"].isin(customers["customer_id"]).all():
        raise ValueError("Orphaned customer_id found in policies table.")
    if not policies["vehicle_id"].isin(vehicles["vehicle_id"]).all():
        raise ValueError("Orphaned vehicle_id found in policies table.")
    if not claims["policy_id"].isin(policies["policy_id"]).all():
        raise ValueError("Orphaned policy_id found in claims table.")
    if not payments["claim_id"].isin(claims["claim_id"]).all():
        raise ValueError("Orphaned claim_id found in payments table.")
    return True

def validate_all_tables(data: dict) -> bool:
    validate_customers(data["customers"])
    validate_vehicles(data["vehicles"])
    validate_policies(data["policies"])
    validate_claims(data["claims"])
    validate_payments(data["payments"])
    validate_relationships(data)
    return True
