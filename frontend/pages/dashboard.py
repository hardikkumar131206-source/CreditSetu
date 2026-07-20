"""Dashboard page for portfolio-level lending insights."""

import streamlit as st

from components.cards import render_kpi_card, render_section_title
from components.visuals import render_approval_trend, render_risk_mix
from utils.sample_data import get_dashboard_metrics, get_portfolio_data


def render_dashboard() -> None:
    """Render the executive dashboard page."""
    metrics = get_dashboard_metrics()
    portfolio = get_portfolio_data()

    render_section_title(
        "Portfolio Command Center",
        "Real-time view of approval quality, risk concentration, and lending volume.",
    )

    columns = st.columns(4)
    for column, metric in zip(columns, metrics):
        with column:
            render_kpi_card(**metric)

    st.markdown('<div class="content-grid two-col">', unsafe_allow_html=True)
    left, right = st.columns([1.45, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Approval Velocity")
        render_approval_trend(portfolio)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Risk Composition")
        render_risk_mix(portfolio)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel table-panel">', unsafe_allow_html=True)
    st.markdown("#### Recent High-Value Applications")
    st.dataframe(
        portfolio[
            [
                "application_id",
                "segment",
                "loan_amount",
                "risk_band",
                "approval_status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
