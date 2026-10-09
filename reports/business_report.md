# Motor Insurance Claims & Policy Analytics — Final Business Report

## 1. Executive Summary
This report delivers an exhaustive analytical evaluation of the motor insurance portfolio managed by the company. Utilizing related operational tables covering customers, vehicles, policies, claims, and payments, this project establishes a robust data pipeline, conducts exploratory data analysis (EDA), tracks core insurance Key Performance Indicators (KPIs), surfaces high-risk business patterns, and provides actionable recommendations to optimize underwriting profitability and operational workflows.

## 2. Business Problem
Insurance management requires continuous oversight to balance aggressive market growth with sound loss-ratio management. Specifically, leadership needed clarity on:
* Policy status distribution (active, expired, cancelled, renewed).
* Premium revenue concentrations across policy types.
* Claim approval and rejection rates alongside overall claim severity.
* Regional and vehicle-specific risk factors driving high-value claim payouts.

## 3. Data and Table Summary
The data architecture relies on five core relational entities stored under data/raw/ and cleaned via automated pipelines into data/cleaned/:
* **Customers**: Captures demographic profile data including age, gender, occupation, and geographic location (state, city).
* **Vehicles**: Stores vehicle attributes (ehicle_type, ehicle_make, ehicle_model, ehicle_year, uel_type, ehicle_value).
* **Policies**: Tracks policy lifecycle dates, coverage limits, premium amounts, status, and payment frequencies.
* **Claims**: Records claim filing dates, accident details, damage severity, and approval/settlement statuses.
* **Payments**: Documents disbursement amounts and payment transaction methods linked to settled claims.

## 4. Data Quality Findings & Cleaning Performed
During initial validation:
* Missing values in numerical attributes were imputed using median metrics, while categorical gaps were standardized to 'Unknown'.
* Duplicate records across primary identifiers (customer_id, policy_id, claim_id, etc.) were successfully eliminated.
* Text columns were stripped of whitespace and capitalized for consistency, and dates were converted to standardized datetime formats.
* Negative outlier values in financial fields were corrected using absolute transformations.

## 5. KPI Summary
* **Total Policies**: Tracked across active and historical portfolios.
* **Active Policies**: Monitored to ensure ongoing recurring revenue streams.
* **Total Premium**: Aggregated premium revenue generated across all policy lines.
* **Claim Approval Rate**: Percentage of approved claims relative to total registered claims.
* **Average Settlement Days**: Operational efficiency metric measuring time elapsed between claim filing and final settlement.
* **Claim-to-Premium Ratio**: Core profitability indicator measuring claim cost relative to premium intake.

## 6. EDA Findings & Important Patterns
* **Vehicle Risk Concentration**: Specific vehicle types (e.g., commercial and high-performance vehicle categories) exhibit disproportionately higher claim severities and payout frequencies.
* **Regional Disparities**: Certain states demonstrate higher claim concentrations, pointing to localized driving hazards or environmental conditions.
* **Settlement Efficiency**: Low-severity claims process rapidly, whereas complex high-value claims experience extended review cycles.

## 7. Business Insights
* **Revenue Drivers**: Standard passenger vehicle policy types generate the vast majority of premium inflows, subsidizing higher-risk segments.
* **Loss Ratio Pressures**: Unfavorable claim-to-premium ratios in select vehicle age brackets threaten underwriting margins if pricing is not adjusted.

## 8. Recommendations
1. **Risk-Based Pricing**: Adjust premium tiers and deductibles upwards for vehicle makes and ages demonstrating high claim-to-premium ratios.
2. **Regional Fraud Detection**: Deploy enhanced investigative workflows in high-claim geographic regions.
3. **Automated Renewals**: Implement automated customer reminder systems targeting policyholders near expiration dates to reduce churn.

## 9. Dashboard & Deployment Summary
* **Interactive Frontend**: Built using Streamlit (pp/streamlit_app.py), enabling dynamic filtering by policy type, status, claim status, vehicle type, and state.
* **DevOps & Cloud**: Containerized via Docker, stored in Amazon ECR, and deployed live on an AWS EC2 instance.

## 10. Conclusion
The implemented analytics pipeline successfully transforms raw operational records into actionable strategic insights, providing management with the tools necessary to optimize loss ratios and drive sustainable profitability.
