"""Reusable card and title components."""

import streamlit as st


def render_section_title(title: str, subtitle: str) -> None:
    """Render a section title block."""
    st.markdown(
        f"""
<div class="section-title">
    <h2>{title}</h2>
    <p>{subtitle}</p>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label: str, value: str, delta: str, tone: str) -> None:
    """Render a KPI card."""
    st.markdown(
        f"""
<div class="kpi-card {tone}">
    <span>{label}</span>
    <strong>{value}</strong>
    <small>{delta}</small>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_card(title: str, message: str, tone: str) -> None:
    """Render an underwriting recommendation card."""
    st.markdown(
        f"""
<div class="recommendation-card {tone}">
    <strong>{title}</strong>
    <p>{message}</p>
</div>
        """,
        unsafe_allow_html=True,
    )
