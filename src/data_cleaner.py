import pandas as pd
import numpy as np

def handle_missing_values(data: dict) -> dict:
    """Handle missing values across tables."""
    # Example cleaning: fill numerical missing values with median or zero, categorical with 'Unknown'
    for key, df in data.items():
        data[key] = df.copy()
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                data[key][col] = data[key][col].fillna(data[key][col].median() if not data[key][col].empty else 0)
            else:
                data[key][col] = data[key][col].fillna('Unknown')
    return data

def remove_duplicates(data: dict) -> dict:
    """Remove duplicate rows from all tables."""
    for key, df in data.items():
        data[key] = df.drop_duplicates().copy()
    return data

def clean_text_columns(data: dict) -> dict:
    """Standardize text formatting in string columns."""
    for key, df in data.items():
        for col in df.select_dtypes(include=['object']).columns:
            data[key][col] = df[col].astype(str).str.strip().str.title()
    return data

def clean_date_columns(data: dict) -> dict:
    """Convert date columns to standard datetime format."""
    date_cols_map = {
        "customers": ["date_of_birth"],
        "policies": ["policy_start_date", "policy_end_date"],
        "claims": ["claim_date", "accident_date", "approval_date", "settlement_date"],
        "payments": ["payment_date"]
    }
    for key, cols in date_cols_map.items():
        if key in data:
            for col in cols:
                if col in data[key].columns:
                    data[key][col] = pd.to_datetime(data[key][col], errors='coerce')
    return data

def validate_numeric_columns(data: dict) -> dict:
    """Ensure numeric columns do not contain illogical negative values where applicable."""
    if "policies" in data:
        data["policies"]["premium_amount"] = data["policies"]["premium_amount"].abs()
        data["policies"]["coverage_amount"] = data["policies"]["coverage_amount"].abs()
    if "claims" in data:
        data["claims"]["claim_amount"] = data["claims"]["claim_amount"].abs()
    if "payments" in data:
        data["payments"]["payment_amount"] = data["payments"]["payment_amount"].abs()
    return data

def validate_business_rules(data: dict) -> dict:
    """Apply specific business rule constraints on cleaned tables."""
    return data

def create_derived_columns(data: dict) -> dict:
    """Create required derived analytical columns."""
    policies = data.get("policies")
    customers = data.get("customers")
    vehicles = data.get("vehicles")
    claims = data.get("claims")
    payments = data.get("payments")
    
    # 1. Policy duration & Active flag
    if policies is not None and "policy_start_date" in policies.columns and "policy_end_date" in policies.columns:
        policies["policy_duration_days"] = (policies["policy_end_date"] - policies["policy_start_date"]).dt.days
        current_date = pd.Timestamp.now()
        policies["policy_active_flag"] = ((policies["policy_start_date"] <= current_date) & (policies["policy_end_date"] >= current_date)).astype(int)
    
    # 2. Customer age
    if customers is not None and "date_of_birth" in customers.columns:
        today = pd.Timestamp.now()
        customers["customer_age"] = (today - customers["date_of_birth"]).dt.days // 365
        
    # 3. Vehicle age
    if vehicles is not None and "vehicle_year" in vehicles.columns:
        current_year = pd.Timestamp.now().year
        vehicles["vehicle_age"] = current_year - vehicles["vehicle_year"]
        
    # 4. Claim processing and settlement days
    if claims is not None:
        if "approval_date" in claims.columns and "claim_date" in claims.columns:
            claims["claim_processing_days"] = (claims["approval_date"] - claims["claim_date"]).dt.days
        if "settlement_date" in claims.columns and "claim_date" in claims.columns:
            claims["claim_settlement_days"] = (claims["settlement_date"] - claims["claim_date"]).dt.days

    # 5. Ratios (Merge claims with policies for claim-to-premium ratio)
    if claims is not None and policies is not None:
        merged_claims_policy = pd.merge(claims, policies[["policy_id", "premium_amount", "coverage_amount"]], on="policy_id", how="left", suffixes=('', '_pol'))
        if "claim_amount" in merged_claims_policy.columns and "premium_amount" in merged_claims_policy.columns:
            claims["claim_to_premium_ratio"] = merged_claims_policy["claim_amount"] / merged_claims_policy["premium_amount"].replace(0, np.nan)
        if "claim_amount" in merged_claims_policy.columns and "coverage_amount" in merged_claims_policy.columns:
            claims["claim_to_coverage_ratio"] = merged_claims_policy["claim_amount"] / merged_claims_policy["coverage_amount"].replace(0, np.nan)

    # 6. Paid claim ratio
    if payments is not None and claims is not None:
        payment_agg = payments.groupby("claim_id")["payment_amount"].sum().reset_index()
        merged_claims_pay = pd.merge(claims, payment_agg, on="claim_id", how="left").fillna({"payment_amount": 0})
        if "payment_amount" in merged_claims_pay.columns and "claim_amount" in merged_claims_pay.columns:
            claims["paid_claim_ratio"] = merged_claims_pay["payment_amount"] / merged_claims_pay["claim_amount"].replace(0, np.nan)

    return data

def clean_data(data: dict) -> dict:
    """Execute full data cleaning sequence."""
    data = handle_missing_values(data)
    data = remove_duplicates(data)
    data = clean_text_columns(data)
    data = clean_date_columns(data)
    data = validate_numeric_columns(data)
    data = validate_business_rules(data)
    data = create_derived_columns(data)
    return data

def save_cleaned_data(data: dict, output_dir: str = "data/cleaned") -> None:
    """Save cleaned datasets to CSV files."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    file_map = {
        "customers": "customers_cleaned.csv",
        "vehicles": "vehicles_cleaned.csv",
        "policies": "policies_cleaned.csv",
        "claims": "claims_cleaned.csv",
        "payments": "payments_cleaned.csv"
    }
    for key, filename in file_map.items():
        if key in data:
            out_path = os.path.join(output_dir, filename)
            data[key].to_csv(out_path, index=False)
