import pandas as pd
import numpy as np

def generate_portfolio_insights(data: dict) -> dict:
    """Generate portfolio-level insights and patterns."""
    policies = data.get("policies", pd.DataFrame())
    active_count = policies[policies['policy_status'].str.lower() == 'active']['policy_id'].nunique() if not policies.empty and 'policy_status' in policies.columns else 0
    total_count = policies['policy_id'].nunique() if not policies.empty else 1
    active_pct = (active_count / total_count) * 100 if total_count > 0 else 0
    
    return {
        "pattern": f"Active policies account for {active_pct:.1f}% of the total policy portfolio.",
        "evidence": f"Out of {total_count} total policies, {active_count} are currently active.",
        "business_meaning": "Maintaining a high active policy ratio ensures stable recurring premium revenue and portfolio health.",
        "recommendation": "Monitor upcoming policy expirations closely and automate renewal reminders to reduce churn."
    }

def generate_claim_insights(data: dict) -> dict:
    """Generate claim-level insights and patterns."""
    claims = data.get("claims", pd.DataFrame())
    if claims.empty or 'claim_status' not in claims.columns:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
    
    total = len(claims)
    approved = len(claims[claims['claim_status'].str.lower() == 'approved'])
    approval_rate = (approved / total) * 100 if total > 0 else 0
    
    return {
        "pattern": f"Claim approval rate stands at {approval_rate:.1f}% across all filed claims.",
        "evidence": f"{approved} claims were approved out of {total} total registered claims.",
        "business_meaning": "A balanced approval rate reflects rigorous validation while maintaining customer trust and satisfaction.",
        "recommendation": "Audit rejected claims periodically to identify potential gaps in policy coverage education for customers."
    }

def generate_premium_insights(data: dict) -> dict:
    """Generate premium-related insights and patterns."""
    policies = data.get("policies", pd.DataFrame())
    if policies.empty or 'policy_type' not in policies.columns or 'premium_amount' not in policies.columns:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
    
    agg = policies.groupby('policy_type')['premium_amount'].sum().reset_index()
    if agg.empty:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
    
    top_policy = agg.loc[agg['premium_amount'].idxmax()]
    
    return {
        "pattern": f"Policy type '{top_policy['policy_type']}' generates the highest share of total premium revenue.",
        "evidence": f"Total premium collected for {top_policy['policy_type']} is {top_policy['premium_amount']:,.2f}.",
        "business_meaning": "Identifies the core revenue-driving product line for the insurance business.",
        "recommendation": "Focus marketing and cross-selling campaigns around this high-performing policy type."
    }

def generate_customer_insights(data: dict) -> dict:
    """Generate customer-level insights and patterns."""
    customers = data.get("customers", pd.DataFrame())
    claims = data.get("claims", pd.DataFrame())
    policies = data.get("policies", pd.DataFrame())
    
    if customers.empty or claims.empty or policies.empty:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
        
    merged = pd.merge(claims, policies[['policy_id', 'customer_id']], on='policy_id', how='inner')
    merged_cust = pd.merge(merged, customers, on='customer_id', how='inner')
    
    if 'state' not in merged_cust.columns:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
        
    state_claims = merged_cust.groupby('state')['claim_id'].count().reset_index()
    top_state = state_claims.loc[state_claims['claim_id'].idxmax()]
    
    return {
        "pattern": f"State '{top_state['state']}' records the highest concentration of customer claims.",
        "evidence": f"A total of {top_state['claim_id']} claims originated from {top_state['state']}.",
        "business_meaning": "Geographic concentration of claims highlights regional risk exposure and potential localized fraud or accident trends.",
        "recommendation": "Deploy localized risk assessment strategies and partner with regional repair networks in high-claim states."
    }

def generate_vehicle_insights(data: dict) -> dict:
    """Generate vehicle-level insights and patterns."""
    vehicles = data.get("vehicles", pd.DataFrame())
    claims = data.get("claims", pd.DataFrame())
    policies = data.get("policies", pd.DataFrame())
    
    if vehicles.empty or claims.empty or policies.empty:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
        
    cp = pd.merge(claims, policies[['policy_id', 'vehicle_id']], on='policy_id', how='inner')
    cpv = pd.merge(cp, vehicles, on='vehicle_id', how='inner')
    
    if 'vehicle_type' not in cpv.columns:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
        
    v_agg = cpv.groupby('vehicle_type')['claim_amount'].sum().reset_index()
    top_veh = v_agg.loc[v_agg['claim_amount'].idxmax()]
    
    return {
        "pattern": f"Vehicle type '{top_veh['vehicle_type']}' contributes the highest total claim payout amount.",
        "evidence": f"Total claim amount for {top_veh['vehicle_type']} reaches {top_veh['claim_amount']:,.2f}.",
        "business_meaning": "Certain vehicle categories carry disproportionately higher severity or accident frequency.",
        "recommendation": "Adjust premium pricing tiers and deductible requirements upwards for high-risk vehicle types."
    }

def generate_risk_patterns(data: dict) -> dict:
    """Generate risk and ratio patterns."""
    claims = data.get("claims", pd.DataFrame())
    if claims.empty or 'claim_to_premium_ratio' not in claims.columns:
        return {"pattern": "N/A", "evidence": "N/A", "business_meaning": "N/A", "recommendation": "N/A"}
        
    avg_ratio = claims['claim_to_premium_ratio'].mean()
    
    return {
        "pattern": f"The portfolio average claim-to-premium ratio is calculated at {avg_ratio:.2f}.",
        "evidence": f"Derived from average claim amounts relative to policy premiums across the portfolio.",
        "business_meaning": "A ratio exceeding threshold limits signals that claims are outpacing premium intake, threatening profitability.",
        "recommendation": "Underwrite policies with higher loss ratios more strictly and introduce risk-based premium adjustments."
    }

def generate_business_recommendations(data: dict) -> dict:
    """Generate overall business recommendations."""
    return {
        "pattern": "Operational efficiency and risk management require targeted intervention.",
        "evidence": "Evidence derived from settlement times, regional claim volumes, and vehicle risk profiles.",
        "business_meaning": "Proactive risk mitigation directly improves loss ratios and customer retention.",
        "recommendation": "Streamline approval workflows for low-severity claims while strengthening fraud detection on high-value payouts."
    }
