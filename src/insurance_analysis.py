import pandas as pd
import numpy as np

# --- 1. Portfolio KPIs ---
def calculate_total_customers(customers: pd.DataFrame) -> int:
    """Calculate total unique customers."""
    return int(customers['customer_id'].nunique()) if not customers.empty else 0

def calculate_total_policies(policies: pd.DataFrame) -> int:
    """Calculate total unique policies."""
    return int(policies['policy_id'].nunique()) if not policies.empty else 0

def calculate_active_policies(policies: pd.DataFrame) -> int:
    """Calculate total active policies."""
    if policies.empty or 'policy_status' not in policies.columns:
        return 0
    return int(policies[policies['policy_status'].str.lower() == 'active']['policy_id'].nunique())

def calculate_expired_policies(policies: pd.DataFrame) -> int:
    """Calculate total expired policies."""
    if policies.empty or 'policy_status' not in policies.columns:
        return 0
    return int(policies[policies['policy_status'].str.lower() == 'expired']['policy_id'].nunique())

def calculate_cancelled_policies(policies: pd.DataFrame) -> int:
    """Calculate total cancelled policies."""
    if policies.empty or 'policy_status' not in policies.columns:
        return 0
    return int(policies[policies['policy_status'].str.lower() == 'cancelled']['policy_id'].nunique())

def calculate_renewed_policies(policies: pd.DataFrame) -> int:
    """Calculate total renewed policies."""
    if policies.empty or 'policy_status' not in policies.columns:
        return 0
    return int(policies[policies['policy_status'].str.lower() == 'renewed']['policy_id'].nunique())


# --- 2. Premium KPIs & Analysis ---
def calculate_total_premium(policies: pd.DataFrame) -> float:
    """Calculate total premium amount."""
    return float(policies['premium_amount'].sum()) if not policies.empty and 'premium_amount' in policies.columns else 0.0

def calculate_average_premium(policies: pd.DataFrame) -> float:
    """Calculate average premium per policy."""
    return float(policies['premium_amount'].mean()) if not policies.empty and 'premium_amount' in policies.columns else 0.0

def calculate_average_coverage(policies: pd.DataFrame) -> float:
    """Calculate average coverage amount per policy."""
    return float(policies['coverage_amount'].mean()) if not policies.empty and 'coverage_amount' in policies.columns else 0.0

def calculate_premium_by_policy_type(policies: pd.DataFrame) -> pd.DataFrame:
    """Calculate total premium aggregated by policy type."""
    if policies.empty or 'policy_type' not in policies.columns:
        return pd.DataFrame()
    return policies.groupby('policy_type')['premium_amount'].sum().reset_index()


# --- 3. Claim KPIs & Analysis ---
def calculate_total_claims(claims: pd.DataFrame) -> int:
    """Calculate total unique claims."""
    return int(claims['claim_id'].nunique()) if not claims.empty else 0

def calculate_approved_claims(claims: pd.DataFrame) -> int:
    """Calculate total approved claims."""
    if claims.empty or 'claim_status' not in claims.columns:
        return 0
    return int(claims[claims['claim_status'].str.lower() == 'approved']['claim_id'].nunique())

def calculate_rejected_claims(claims: pd.DataFrame) -> int:
    """Calculate total rejected claims."""
    if claims.empty or 'claim_status' not in claims.columns:
        return 0
    return int(claims[claims['claim_status'].str.lower() == 'rejected']['claim_id'].nunique())

def calculate_pending_claims(claims: pd.DataFrame) -> int:
    """Calculate total pending claims."""
    if claims.empty or 'claim_status' not in claims.columns:
        return 0
    return int(claims[claims['claim_status'].str.lower() == 'pending']['claim_id'].nunique())

def calculate_total_claim_amount(claims: pd.DataFrame) -> float:
    """Calculate total claim amount requested."""
    return float(claims['claim_amount'].sum()) if not claims.empty and 'claim_amount' in claims.columns else 0.0

def calculate_average_claim_amount(claims: pd.DataFrame) -> float:
    """Calculate average claim amount requested."""
    return float(claims['claim_amount'].mean()) if not claims.empty and 'claim_amount' in claims.columns else 0.0

def calculate_claim_approval_rate(claims: pd.DataFrame) -> float:
    """Calculate percentage of approved claims out of total claims."""
    total = calculate_total_claims(claims)
    if total == 0:
        return 0.0
    approved = calculate_approved_claims(claims)
    return float((approved / total) * 100)

def calculate_claim_rejection_rate(claims: pd.DataFrame) -> float:
    """Calculate percentage of rejected claims out of total claims."""
    total = calculate_total_claims(claims)
    if total == 0:
        return 0.0
    rejected = calculate_rejected_claims(claims)
    return float((rejected / total) * 100)


# --- 4. Settlement & Operational Metrics ---
def calculate_average_claim_processing_days(claims: pd.DataFrame) -> float:
    """Calculate average processing days from claim date to approval date."""
    if claims.empty or 'claim_processing_days' not in claims.columns:
        return 0.0
    return float(claims['claim_processing_days'].mean())

def calculate_average_claim_settlement_days(claims: pd.DataFrame) -> float:
    """Calculate average settlement days from claim date to settlement date."""
    if claims.empty or 'claim_settlement_days' not in claims.columns:
        return 0.0
    return float(claims['claim_settlement_days'].mean())

def calculate_total_payment_amount(payments: pd.DataFrame) -> float:
    """Calculate total payment amount paid toward claims."""
    return float(payments['payment_amount'].sum()) if not payments.empty and 'payment_amount' in payments.columns else 0.0

def calculate_average_payment_amount(payments: pd.DataFrame) -> float:
    """Calculate average payment amount."""
    return float(payments['payment_amount'].mean()) if not payments.empty and 'payment_amount' in payments.columns else 0.0


# --- 5. Risk & Ratios ---
def calculate_claim_to_premium_ratio(claims: pd.DataFrame) -> float:
    """Calculate average claim-to-premium ratio."""
    if claims.empty or 'claim_to_premium_ratio' not in claims.columns:
        return 0.0
    return float(claims['claim_to_premium_ratio'].mean())

def calculate_claim_to_coverage_ratio(claims: pd.DataFrame) -> float:
    """Calculate average claim-to-coverage ratio."""
    if claims.empty or 'claim_to_coverage_ratio' not in claims.columns:
        return 0.0
    return float(claims['claim_to_coverage_ratio'].mean())

def calculate_paid_claim_ratio(claims: pd.DataFrame) -> float:
    """Calculate average paid claim ratio."""
    if claims.empty or 'paid_claim_ratio' not in claims.columns:
        return 0.0
    return float(claims['paid_claim_ratio'].mean())


# --- 6. Customer, Vehicle & Business Breakdowns ---
def analyze_customer_claims(claims: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Analyze claim frequency and amounts per customer."""
    if claims.empty or customers.empty:
        return pd.DataFrame()
    merged = pd.merge(claims, customers, on='customer_id', how='inner')
    return merged.groupby(['customer_id', 'customer_name']).agg(
        total_claims=('claim_id', 'count'),
        total_claimed_amount=('claim_amount', 'sum')
    ).reset_index()

def analyze_customer_premium(policies: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Analyze premium paid per customer."""
    if policies.empty or customers.empty:
        return pd.DataFrame()
    merged = pd.merge(policies, customers, on='customer_id', how='inner')
    return merged.groupby(['customer_id', 'customer_name']).agg(
        total_policies=('policy_id', 'count'),
        total_premium=('premium_amount', 'sum')
    ).reset_index()

def analyze_vehicle_claims(claims: pd.DataFrame, policies: pd.DataFrame, vehicles: pd.DataFrame) -> pd.DataFrame:
    """Analyze claims grouped by vehicle type and make."""
    if claims.empty or policies.empty or vehicles.empty:
        return pd.DataFrame()
    cp = pd.merge(claims, policies[['policy_id', 'vehicle_id']], on='policy_id', how='inner')
    cpv = pd.merge(cp, vehicles, on='vehicle_id', how='inner')
    return cpv.groupby(['vehicle_type', 'vehicle_make']).agg(
        claim_count=('claim_id', 'count'),
        total_claim_amount=('claim_amount', 'sum'),
        avg_claim_amount=('claim_amount', 'mean')
    ).reset_index()

def analyze_vehicle_risk_patterns(vehicles: pd.DataFrame, claims: pd.DataFrame, policies: pd.DataFrame) -> pd.DataFrame:
    """Analyze vehicle age groups or risk patterns against claims."""
    if vehicles.empty or claims.empty or policies.empty:
        return pd.DataFrame()
    cp = pd.merge(claims, policies[['policy_id', 'vehicle_id']], on='policy_id', how='inner')
    cpv = pd.merge(cp, vehicles, on='vehicle_id', how='inner')
    if 'vehicle_age' not in cpv.columns:
        cpv['vehicle_age'] = 0
    return cpv.groupby('vehicle_age').agg(
        claim_count=('claim_id', 'count'),
        total_claim_amount=('claim_amount', 'sum')
    ).reset_index()

def analyze_claim_type(claims: pd.DataFrame) -> pd.DataFrame:
    """Analyze claims grouped by claim type."""
    if claims.empty or 'claim_type' not in claims.columns:
        return pd.DataFrame()
    return claims.groupby('claim_type').agg(
        claim_count=('claim_id', 'count'),
        total_amount=('claim_amount', 'sum'),
        avg_amount=('claim_amount', 'mean')
    ).reset_index()

def analyze_claim_status(claims: pd.DataFrame) -> pd.DataFrame:
    """Analyze claims grouped by claim status."""
    if claims.empty or 'claim_status' not in claims.columns:
        return pd.DataFrame()
    return claims.groupby('claim_status').agg(
        claim_count=('claim_id', 'count'),
        total_amount=('claim_amount', 'sum')
    ).reset_index()

def analyze_policy_type(policies: pd.DataFrame) -> pd.DataFrame:
    """Analyze policies grouped by policy type."""
    if policies.empty or 'policy_type' not in policies.columns:
        return pd.DataFrame()
    return policies.groupby('policy_type').agg(
        policy_count=('policy_id', 'count'),
        total_premium=('premium_amount', 'sum'),
        avg_premium=('premium_amount', 'mean')
    ).reset_index()

def analyze_region(customers: pd.DataFrame, claims: pd.DataFrame, policies: pd.DataFrame) -> pd.DataFrame:
    """Analyze claim and premium metrics by geographic region (State/City)."""
    if customers.empty:
        return pd.DataFrame()
    return customers.groupby(['state', 'city']).agg(
        customer_count=('customer_id', 'count')
    ).reset_index()

def analyze_vehicle_type(vehicles: pd.DataFrame) -> pd.DataFrame:
    """Analyze vehicle attributes by type."""
    if vehicles.empty or 'vehicle_type' not in vehicles.columns:
        return pd.DataFrame()
    return vehicles.groupby('vehicle_type').agg(
        vehicle_count=('vehicle_id', 'count'),
        avg_vehicle_value=('vehicle_value', 'mean')
    ).reset_index()

def analyze_damage_severity(claims: pd.DataFrame) -> pd.DataFrame:
    """Analyze claims categorized by damage severity."""
    if claims.empty or 'damage_severity' not in claims.columns:
        return pd.DataFrame()
    return claims.groupby('damage_severity').agg(
        claim_count=('claim_id', 'count'),
        total_claim_amount=('claim_amount', 'sum'),
        avg_claim_amount=('claim_amount', 'mean')
    ).reset_index()
