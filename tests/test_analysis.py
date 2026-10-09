import pytest
import pandas as pd
from src.insurance_analysis import calculate_total_policies, calculate_active_policies, calculate_total_claims, calculate_total_premium, calculate_claim_approval_rate

def test_calculate_total_policies():
    df = pd.DataFrame({"policy_id": ["POL_01", "POL_02", "POL_03"]})
    assert calculate_total_policies(df) == 3

def test_calculate_active_policies():
    df = pd.DataFrame({
        "policy_id": ["POL_01", "POL_02"],
        "policy_status": ["Active", "Expired"]
    })
    assert calculate_active_policies(df) == 1

def test_calculate_total_claims():
    df = pd.DataFrame({"claim_id": ["CLM_01", "CLM_02"]})
    assert calculate_total_claims(df) == 2

def test_calculate_total_premium():
    df = pd.DataFrame({"premium_amount": [500.0, 1000.0]})
    assert calculate_total_premium(df) == 1500.0

def test_calculate_claim_approval_rate():
    df = pd.DataFrame({
        "claim_id": ["CLM_01", "CLM_02", "CLM_03", "CLM_04"],
        "claim_status": ["Approved", "Approved", "Rejected", "Pending"]
    })
    assert calculate_claim_approval_rate(df) == 50.0
