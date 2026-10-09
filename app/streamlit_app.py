import streamlit as st
import pandas as pd
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.insurance_analysis import (
    calculate_total_customers, calculate_total_policies, calculate_active_policies,
    calculate_expired_policies, calculate_cancelled_policies, calculate_renewed_policies,
    calculate_total_premium, calculate_average_premium, calculate_average_coverage,
    calculate_total_claims, calculate_approved_claims, calculate_rejected_claims,
    calculate_pending_claims, calculate_total_claim_amount, calculate_average_claim_amount,
    calculate_claim_approval_rate, calculate_claim_rejection_rate,
    calculate_average_claim_processing_days, calculate_average_claim_settlement_days,
    calculate_total_payment_amount, calculate_claim_to_premium_ratio
)
from src.insights import (
    generate_portfolio_insights, generate_claim_insights, generate_premium_insights,
    generate_customer_insights, generate_vehicle_insights, generate_risk_patterns,
    generate_business_recommendations
)
from src.visualization import (
    plot_policy_status, plot_policy_type_distribution, plot_premium_by_policy_type,
    plot_monthly_claims, plot_claim_status, plot_claim_type_distribution,
    plot_claim_amount_distribution, plot_claim_amount_by_vehicle_type,
    plot_claims_by_region, plot_claim_severity_by_region, plot_average_settlement_time,
    plot_claim_to_premium_by_policy_type, plot_vehicle_age_vs_claim_amount,
    plot_customer_age_vs_claim_amount, plot_vehicle_type_claim_performance,
    plot_damage_severity_distribution, plot_payment_status, plot_monthly_premium_trend
)

st.set_page_config(page_title="Motor Insurance Analytics Dashboard", layout="wide")

@st.cache_data
def load_dashboard_data():
    """Load cleaned datasets."""
    cleaned_dir = "data/cleaned"
    try:
        customers = pd.read_csv(os.path.join(cleaned_dir, "customers_cleaned.csv"))
        vehicles = pd.read_csv(os.path.join(cleaned_dir, "vehicles_cleaned.csv"))
        policies = pd.read_csv(os.path.join(cleaned_dir, "policies_cleaned.csv"))
        claims = pd.read_csv(os.path.join(cleaned_dir, "claims_cleaned.csv"))
        payments = pd.read_csv(os.path.join(cleaned_dir, "payments_cleaned.csv"))
        
        # Parse dates
        for df, cols in [(customers, ['date_of_birth']), 
                         (policies, ['policy_start_date', 'policy_end_date']),
                         (claims, ['claim_date', 'accident_date', 'approval_date', 'settlement_date']),
                         (payments, ['payment_date'])]:
            for c in cols:
                if c in df.columns:
                    df[c] = pd.to_datetime(df[c], errors='coerce')
        return customers, vehicles, policies, claims, payments
    except Exception as e:
        st.error(f"Error loading cleaned data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

customers, vehicles, policies, claims, payments = load_dashboard_data()

def show_sidebar_filters():
    """Render interactive sidebar filters."""
    st.sidebar.header("🔍 Dashboard Filters")
    
    policy_types = policies['policy_type'].dropna().unique().tolist() if 'policy_type' in policies.columns else []
    selected_policy_types = st.sidebar.multiselect("Policy Type", policy_types, default=policy_types)
    
    policy_statuses = policies['policy_status'].dropna().unique().tolist() if 'policy_status' in policies.columns else []
    selected_policy_statuses = st.sidebar.multiselect("Policy Status", policy_statuses, default=policy_statuses)
    
    claim_statuses = claims['claim_status'].dropna().unique().tolist() if 'claim_status' in claims.columns else []
    selected_claim_statuses = st.sidebar.multiselect("Claim Status", claim_statuses, default=claim_statuses)
    
    vehicle_types = vehicles['vehicle_type'].dropna().unique().tolist() if 'vehicle_type' in vehicles.columns else []
    selected_vehicle_types = st.sidebar.multiselect("Vehicle Type", vehicle_types, default=vehicle_types)
    
    states = customers['state'].dropna().unique().tolist() if 'state' in customers.columns else []
    selected_states = st.sidebar.multiselect("State / Region", states, default=states)
    
    # Filter datasets
    filtered_policies = policies[policies['policy_type'].isin(selected_policy_types) & policies['policy_status'].isin(selected_policy_statuses)] if not policies.empty else policies
    filtered_claims = claims[claims['claim_status'].isin(selected_claim_statuses)] if not claims.empty else claims
    filtered_vehicles = vehicles[vehicles['vehicle_type'].isin(selected_vehicle_types)] if not vehicles.empty else vehicles
    filtered_customers = customers[customers['state'].isin(selected_states)] if not customers.empty else customers
    
    return filtered_customers, filtered_vehicles, filtered_policies, filtered_claims, payments

f_cust, f_veh, f_pol, f_claims, f_pay = show_sidebar_filters()

def show_overview():
    st.title("📊 Executive Overview")
    st.markdown("High-level summary of motor insurance portfolio, premium revenue, and claim performance.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Policies", calculate_total_policies(f_pol))
    col2.metric("Active Policies", calculate_active_policies(f_pol))
    col3.metric("Total Premium", f"")
    col4.metric("Total Claims", calculate_total_claims(f_claims))
    
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Total Claim Amount", f"")
    col6.metric("Approval Rate", f"{calculate_claim_approval_rate(f_claims):.1f}%")
    col7.metric("Avg Settlement Days", f"{calculate_average_claim_settlement_days(f_claims):.1f} days")
    col8.metric("Claim-to-Premium Ratio", f"{calculate_claim_to_premium_ratio(f_claims):.2f}")
    
    st.markdown("---")
    st.subheader("Quick Portfolio Trend & Status")
    plot_policy_status(f_pol)
    if os.path.exists("reports/figures/policy_status_distribution.png"):
        st.image("reports/figures/policy_status_distribution.png")

def show_policy_analysis():
    st.title("📁 Policy Analysis")
    st.markdown("Explore policy distribution, types, status breakdowns, and monthly premium trends.")
    
    col1, col2 = st.columns(2)
    with col1:
        plot_policy_type_distribution(f_pol)
        if os.path.exists("reports/figures/policy_type_distribution.png"):
            st.image("reports/figures/policy_type_distribution.png")
    with col2:
        plot_premium_by_policy_type(f_pol)
        if os.path.exists("reports/figures/premium_by_policy_type.png"):
            st.image("reports/figures/premium_by_policy_type.png")
            
    plot_monthly_premium_trend(f_pol)
    if os.path.exists("reports/figures/monthly_premium_trend.png"):
        st.image("reports/figures/monthly_premium_trend.png")

def show_claim_analysis():
    st.title("⚠️ Claims Analysis")
    st.markdown("Analyze claim volumes, approval statuses, claim types, and severity distributions.")
    
    col1, col2 = st.columns(2)
    with col1:
        plot_claim_status(f_claims)
        if os.path.exists("reports/figures/claim_status_distribution.png"):
            st.image("reports/figures/claim_status_distribution.png")
    with col2:
        plot_claim_type_distribution(f_claims)
        if os.path.exists("reports/figures/claim_type_distribution.png"):
            st.image("reports/figures/claim_type_distribution.png")
            
    plot_monthly_claims(f_claims)
    if os.path.exists("reports/figures/monthly_claims_trend.png"):
        st.image("reports/figures/monthly_claims_trend.png")

def show_customer_analysis():
    st.title("👤 Customer Analysis")
    st.markdown("Examine customer demographics, regional distributions, and age impact on claims.")
    
    plot_claims_by_region(f_cust, f_claims, f_pol)
    if os.path.exists("reports/figures/claims_by_region.png"):
        st.image("reports/figures/claims_by_region.png")
        
    plot_customer_age_vs_claim_amount(f_cust, f_claims, f_pol)
    if os.path.exists("reports/figures/customer_age_vs_claim_amount.png"):
        st.image("reports/figures/customer_age_vs_claim_amount.png")

def show_vehicle_analysis():
    st.title("🚗 Vehicle Analysis")
    st.markdown("Investigate claim performance across vehicle types, makes, and vehicle ages.")
    
    col1, col2 = st.columns(2)
    with col1:
        plot_vehicle_type_claim_performance(f_veh, f_claims, f_pol)
        if os.path.exists("reports/figures/vehicle_type_claim_performance.png"):
            st.image("reports/figures/vehicle_type_claim_performance.png")
    with col2:
        plot_damage_severity_distribution(f_claims)
        if os.path.exists("reports/figures/damage_severity_distribution.png"):
            st.image("reports/figures/damage_severity_distribution.png")
            
    plot_vehicle_age_vs_claim_amount(f_veh, f_claims, f_pol)
    if os.path.exists("reports/figures/vehicle_age_vs_claim_amount.png"):
        st.image("reports/figures/vehicle_age_vs_claim_amount.png")

def show_premium_analysis():
    st.title("💰 Premium & Risk Analysis")
    st.markdown("Evaluate claim-to-premium ratios, coverage amounts, and risk patterns.")
    
    plot_claim_to_premium_by_policy_type(f_claims, f_pol)
    if os.path.exists("reports/figures/claim_to_premium_by_policy_type.png"):
        st.image("reports/figures/claim_to_premium_by_policy_type.png")
        
    plot_claim_severity_by_region(f_cust, f_claims, f_pol)
    if os.path.exists("reports/figures/claim_severity_by_region.png"):
        st.image("reports/figures/claim_severity_by_region.png")

def show_insights():
    st.title("💡 Insights & Recommendations")
    st.markdown("Strategic business patterns, evidence, and actionable recommendations.")
    
    data_dict = {"policies": f_pol, "claims": f_claims, "customers": f_cust, "vehicles": f_veh}
    
    insights_list = [
        ("Portfolio Health Insight", generate_portfolio_insights(data_dict)),
        ("Claim Performance Insight", generate_claim_insights(data_dict)),
        ("Premium Revenue Insight", generate_premium_insights(data_dict)),
        ("Customer & Regional Insight", generate_customer_insights(data_dict)),
        ("Vehicle Risk Insight", generate_vehicle_insights(data_dict)),
        ("Risk & Ratio Insight", generate_risk_patterns(data_dict))
    ]
    
    for title, ins in insights_list:
        with st.expander(title, expanded=True):
            st.markdown(f"**PATTERN:** {ins.get('pattern')}")
            st.markdown(f"**EVIDENCE:** {ins.get('evidence')}")
            st.markdown(f"**BUSINESS MEANING:** {ins.get('business_meaning')}")
            st.markdown(f"**RECOMMENDATION:** {ins.get('recommendation')}")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Executive Overview", 
        "Policy Analysis", 
        "Claims Analysis", 
        "Customer Analysis", 
        "Vehicle Analysis", 
        "Premium & Risk", 
        "Insights & Recommendations"
    ])
    
    if page == "Executive Overview":
        show_overview()
    elif page == "Policy Analysis":
        show_policy_analysis()
    elif page == "Claims Analysis":
        show_claim_analysis()
    elif page == "Customer Analysis":
        show_customer_analysis()
    elif page == "Vehicle Analysis":
        show_vehicle_analysis()
    elif page == "Premium & Risk":
        show_premium_analysis()
    elif page == "Insights & Recommendations":
        show_insights()

if __name__ == "__main__":
    main()
