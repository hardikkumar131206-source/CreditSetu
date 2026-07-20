"""Stable sidebar navigation component."""

import streamlit as st


def render_sidebar(pages: list[str]) -> str:
    """Render the fixed navigation sidebar and return the selected page."""
    with st.sidebar:
        st.markdown(
            """
<div class="brand-block">
    <div class="brand-mark">CS</div>
    <div>
        <div class="brand-name">CreditSetu AI</div>
        <div class="brand-subtitle">Loan Intelligence</div>
    </div>
</div>
            """,
            unsafe_allow_html=True,
        )
        selected_page = st.radio(
            "Navigation",
            pages,
            label_visibility="visible",
            key="primary_navigation",
        )
        st.markdown(
            """
<div class="sidebar-footer">
    <span class="status-dot"></span>
    Frontend architecture online
</div>
            """,
            unsafe_allow_html=True,
        )
    return selected_page
