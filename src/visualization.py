import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set plotting style
sns.set_theme(style="whitegrid")
os.makedirs("reports/figures", exist_ok=True)

def save_and_show_plot(fig, filename: str):
    """Save plot to reports/figures and close."""
    fig.savefig(os.path.join("reports/figures", filename), bbox_inches="tight", dpi=300)
    plt.close(fig)

def plot_policy_status(policies: pd.DataFrame):
    """Plot policy status distribution."""
    if policies.empty or 'policy_status' not in policies.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=policies, x='policy_status', palette='Blues_r', ax=ax)
    ax.set_title("Policy Status Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Policy Status", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    save_and_show_plot(fig, "policy_status_distribution.png")

def plot_policy_type_distribution(policies: pd.DataFrame):
    """Plot policy type distribution."""
    if policies.empty or 'policy_type' not in policies.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=policies, x='policy_type', palette='viridis', ax=ax)
    ax.set_title("Policy Type Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Policy Type", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    save_and_show_plot(fig, "policy_type_distribution.png")

def plot_premium_by_policy_type(policies: pd.DataFrame):
    """Plot total premium by policy type."""
    if policies.empty or 'policy_type' not in policies.columns or 'premium_amount' not in policies.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    agg = policies.groupby('policy_type')['premium_amount'].sum().reset_index()
    sns.barplot(data=agg, x='policy_type', y='premium_amount', palette='magma', ax=ax)
    ax.set_title("Total Premium by Policy Type", fontsize=14, fontweight='bold')
    ax.set_xlabel("Policy Type", fontsize=12)
    ax.set_ylabel("Total Premium Amount", fontsize=12)
    save_and_show_plot(fig, "premium_by_policy_type.png")

def plot_monthly_claims(claims: pd.DataFrame):
    """Plot monthly claims trend."""
    if claims.empty or 'claim_date' not in claims.columns:
        return
    claims_copy = claims.copy()
    claims_copy['claim_month'] = claims_copy['claim_date'].dt.to_period('M').astype(str)
    agg = claims_copy.groupby('claim_month').size().reset_index(name='claim_count')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=agg, x='claim_month', y='claim_count', marker='o', color='b', ax=ax)
    ax.set_title("Monthly Claims Trend", fontsize=14, fontweight='bold')
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Claim Count", fontsize=12)
    plt.xticks(rotation=45)
    save_and_show_plot(fig, "monthly_claims_trend.png")

def plot_claim_status(claims: pd.DataFrame):
    """Plot claim status distribution."""
    if claims.empty or 'claim_status' not in claims.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=claims, x='claim_status', palette='Set2', ax=ax)
    ax.set_title("Claim Status Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Claim Status", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    save_and_show_plot(fig, "claim_status_distribution.png")

def plot_claim_type_distribution(claims: pd.DataFrame):
    """Plot claim type distribution."""
    if claims.empty or 'claim_type' not in claims.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=claims, x='claim_type', palette='Spectral', ax=ax)
    ax.set_title("Claim Type Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Claim Type", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    save_and_show_plot(fig, "claim_type_distribution.png")

def plot_claim_amount_distribution(claims: pd.DataFrame):
    """Plot claim amount distribution."""
    if claims.empty or 'claim_amount' not in claims.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(claims['claim_amount'], kde=True, color='purple', bins=30, ax=ax)
    ax.set_title("Claim Amount Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Claim Amount", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    save_and_show_plot(fig, "claim_amount_distribution.png")

def plot_claim_amount_by_vehicle_type(claims: pd.DataFrame, policies: pd.DataFrame, vehicles: pd.DataFrame):
    """Plot claim amount grouped by vehicle type."""
    if claims.empty or policies.empty or vehicles.empty:
        return
    cp = pd.merge(claims, policies[['policy_id', 'vehicle_id']], on='policy_id', how='inner')
    cpv = pd.merge(cp, vehicles, on='vehicle_id', how='inner')
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=cpv, x='vehicle_type', y='claim_amount', palette='Set3', ax=ax)
    ax.set_title("Claim Amount by Vehicle Type", fontsize=14, fontweight='bold')
    ax.set_xlabel("Vehicle Type", fontsize=12)
    ax.set_ylabel("Claim Amount", fontsize=12)
    save_and_show_plot(fig, "claim_amount_by_vehicle_type.png")

def plot_claims_by_region(customers: pd.DataFrame, claims: pd.DataFrame, policies: pd.DataFrame):
    """Plot claims by region (State)."""
    if customers.empty or claims.empty or policies.empty:
        return
    cp = pd.merge(claims, policies[['policy_id', 'customer_id']], on='policy_id', how='inner', suffixes=('', '_pol'))
    cpc = pd.merge(cp, customers, on='customer_id', how='inner')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=cpc, x='state', order=cpc['state'].value_counts().index, palette='crest', ax=ax)
    ax.set_title("Claim Count by Region (State)", fontsize=14, fontweight='bold')
    ax.set_xlabel("State", fontsize=12)
    ax.set_ylabel("Claim Count", fontsize=12)
    plt.xticks(rotation=45)
    save_and_show_plot(fig, "claims_by_region.png")

def plot_claim_severity_by_region(customers: pd.DataFrame, claims: pd.DataFrame, policies: pd.DataFrame):
    """Plot average claim amount by region (State)."""
    if customers.empty or claims.empty or policies.empty:
        return
    cp = pd.merge(claims, policies[['policy_id', 'customer_id']], on='policy_id', how='inner', suffixes=('', '_pol'))
    cpc = pd.merge(cp, customers, on='customer_id', how='inner')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=cpc, x='state', y='claim_amount', estimator=lambda x: sum(x) / len(x), palette='rocket', ax=ax)
    ax.set_title("Average Claim Severity by Region (State)", fontsize=14, fontweight='bold')
    ax.set_xlabel("State", fontsize=12)
    ax.set_ylabel("Average Claim Amount", fontsize=12)
    plt.xticks(rotation=45)
    save_and_show_plot(fig, "claim_severity_by_region.png")

def plot_average_settlement_time(claims: pd.DataFrame):
    """Plot claim settlement time distribution."""
    if claims.empty or 'claim_settlement_days' not in claims.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(claims['claim_settlement_days'].dropna(), kde=True, color='teal', bins=30, ax=ax)
    ax.set_title("Claim Settlement Days Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Settlement Days", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    save_and_show_plot(fig, "average_settlement_time.png")

def plot_claim_to_premium_by_policy_type(claims: pd.DataFrame, policies: pd.DataFrame):
    """Plot claim-to-premium ratio by policy type."""
    if claims.empty or policies.empty:
        return
    merged = pd.merge(claims, policies, on='policy_id', how='inner')
    if 'claim_to_premium_ratio' not in merged.columns:
        return
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=merged, x='policy_type', y='claim_to_premium_ratio', palette='cubehelix', ax=ax)
    ax.set_title("Claim-to-Premium Ratio by Policy Type", fontsize=14, fontweight='bold')
    ax.set_xlabel("Policy Type", fontsize=12)
    ax.set_ylabel("Claim-to-Premium Ratio", fontsize=12)
    save_and_show_plot(fig, "claim_to_premium_by_policy_type.png")

def plot_vehicle_age_vs_claim_amount(vehicles: pd.DataFrame, claims: pd.DataFrame, policies: pd.DataFrame):
    """Plot vehicle age versus claim amount."""
    if vehicles.empty or claims.empty or policies.empty:
        return
    cp = pd.merge(claims, policies[['policy_id', 'vehicle_id']], on='policy_id', how='inner')
    cpv = pd.merge(cp, vehicles, on='vehicle_id', how='inner')
    if 'vehicle_age' not in cpv.columns:
        return
        
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=cpv, x='vehicle_age', y='claim_amount', alpha=0.6, color='darkorange', ax=ax)
    ax.set_title("Vehicle Age vs Claim Amount", fontsize=14, fontweight='bold')
    ax.set_xlabel("Vehicle Age (Years)", fontsize=12)
    ax.set_ylabel("Claim Amount", fontsize=12)
    save_and_show_plot(fig, "vehicle_age_vs_claim_amount.png")

def plot_customer_age_vs_claim_amount(customers: pd.DataFrame, claims: pd.DataFrame, policies: pd.DataFrame):
    """Plot customer age versus claim amount."""
    if customers.empty or claims.empty or policies.empty:
        return
    cp = pd.merge(claims, policies[['policy_id', 'customer_id']], on='policy_id', how='inner', suffixes=('', '_pol'))
    cpc = pd.merge(cp, customers, on='customer_id', how='inner')
    if 'customer_age' not in cpc.columns:
        return
        
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=cpc, x='customer_age', y='claim_amount', alpha=0.6, color='purple', ax=ax)
    ax.set_title("Customer Age vs Claim Amount", fontsize=14, fontweight='bold')
    ax.set_xlabel("Customer Age", fontsize=12)
    ax.set_ylabel("Claim Amount", fontsize=12)
    save_and_show_plot(fig, "customer_age_vs_claim_amount.png")

def plot_vehicle_type_claim_performance(vehicles: pd.DataFrame, claims: pd.DataFrame, policies: pd.DataFrame):
    """Plot claim performance by vehicle type."""
    if vehicles.empty or claims.empty or policies.empty:
        return
    cp = pd.merge(claims, policies[['policy_id', 'vehicle_id']], on='policy_id', how='inner')
    cpv = pd.merge(cp, vehicles, on='vehicle_id', how='inner')
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cpv, x='vehicle_type', y='claim_amount', estimator=sum, palette='viridis', ax=ax)
    ax.set_title("Total Claim Amount by Vehicle Type", fontsize=14, fontweight='bold')
    ax.set_xlabel("Vehicle Type", fontsize=12)
    ax.set_ylabel("Total Claim Amount", fontsize=12)
    save_and_show_plot(fig, "vehicle_type_claim_performance.png")

def plot_damage_severity_distribution(claims: pd.DataFrame):
    """Plot damage severity distribution."""
    if claims.empty or 'damage_severity' not in claims.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=claims, x='damage_severity', order=['Low', 'Medium', 'High'], palette='coolwarm', ax=ax)
    ax.set_title("Damage Severity Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Damage Severity", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    save_and_show_plot(fig, "damage_severity_distribution.png")

def plot_payment_status(payments: pd.DataFrame):
    """Plot payment status distribution."""
    if payments.empty or 'payment_status' not in payments.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=payments, x='payment_status', palette='pastel', ax=ax)
    ax.set_title("Payment Status Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Payment Status", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    save_and_show_plot(fig, "payment_status_distribution.png")

def plot_monthly_premium_trend(policies: pd.DataFrame):
    """Plot monthly premium collection trend."""
    if policies.empty or 'policy_start_date' not in policies.columns:
        return
    p_copy = policies.copy()
    p_copy['start_month'] = p_copy['policy_start_date'].dt.to_period('M').astype(str)
    agg = p_copy.groupby('start_month')['premium_amount'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=agg, x='start_month', y='premium_amount', marker='s', color='green', ax=ax)
    ax.set_title("Monthly Premium Collection Trend", fontsize=14, fontweight='bold')
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Premium Amount", fontsize=12)
    plt.xticks(rotation=45)
    save_and_show_plot(fig, "monthly_premium_trend.png")
