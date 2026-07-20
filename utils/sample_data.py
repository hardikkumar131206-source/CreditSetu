"""Static sample data used only by the frontend scaffold."""

import pandas as pd


def get_dashboard_metrics() -> list[dict[str, str]]:
    """Return static dashboard KPI cards."""
    return [
        {"label": "Applications", "value": "1,284", "delta": "+18.4% MoM", "tone": "blue"},
        {"label": "Approval Rate", "value": "72.6%", "delta": "+3.1 pts", "tone": "green"},
        {"label": "Avg. Ticket", "value": "$48.2K", "delta": "+$2.7K", "tone": "purple"},
        {"label": "Risk Alerts", "value": "37", "delta": "-9 today", "tone": "pink"},
    ]


def get_portfolio_data() -> pd.DataFrame:
    """Return sample lending portfolio data."""
    return pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "approval_rate": [64, 67, 66, 70, 71, 73],
            "application_id": [
                "CS-APP-1024",
                "CS-APP-1025",
                "CS-APP-1026",
                "CS-APP-1027",
                "CS-APP-1028",
                "CS-APP-1029",
            ],
            "segment": ["Prime", "Near Prime", "Prime", "SME", "Retail", "SME"],
            "loan_amount": [125000, 82000, 67500, 212000, 39000, 176000],
            "risk_band": ["Low", "Medium", "Low", "High", "Medium", "High"],
            "approval_status": ["Approved", "Review", "Approved", "Review", "Approved", "Declined"],
        }
    )


def get_application_history() -> pd.DataFrame:
    """Return sample application history."""
    return pd.DataFrame(
        {
            "Application ID": ["CS-APP-1024", "CS-APP-1025", "CS-APP-1026", "CS-APP-1027"],
            "Borrower": ["Avery Stone", "Maya Chen", "Jordan Lee", "Rina Patel"],
            "Loan Amount": ["$125,000", "$82,000", "$67,500", "$212,000"],
            "Risk Band": ["Low", "Medium", "Low", "High"],
            "Status": ["Approved", "Review", "Approved", "Declined"],
            "Channel": ["Branch", "Mobile", "Partner", "Branch"],
            "Updated": ["Today", "Today", "Yesterday", "Yesterday"],
        }
    )


def get_feature_impact_data() -> pd.DataFrame:
    """Return static feature impact values for UI preview."""
    return pd.DataFrame(
        {
            "feature": [
                "Credit Score",
                "Debt-to-Income",
                "Annual Income",
                "Loan Amount",
                "Employment Tenure",
                "Collateral Quality",
            ],
            "impact": [0.22, -0.16, 0.14, -0.09, 0.07, 0.05],
        }
    )


def get_fairness_data() -> pd.DataFrame:
    """Return static fairness-monitoring data."""
    return pd.DataFrame(
        {
            "segment": ["Urban", "Semiurban", "Rural", "New-to-Credit", "SME"],
            "approval_rate": [0.76, 0.71, 0.66, 0.61, 0.68],
            "baseline_rate": [0.72, 0.72, 0.72, 0.72, 0.72],
            "gap": [0.04, -0.01, -0.06, -0.11, -0.04],
            "status": ["Healthy", "Healthy", "Watch", "Review", "Watch"],
        }
    )
