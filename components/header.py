"""Page header component."""

import streamlit as st


def render_header(active_page: str) -> None:
    """Render a premium app header for the active page."""
    st.markdown(
        f"""
<div class="app-header">
    <div>
        <p class="eyebrow">Commercial Banking Dashboard</p>
        <h1>{active_page}</h1>
    </div>
    <div class="header-actions">
        <span class="pill">Production UI</span>
        <span class="pill accent">Dark Fintech</span>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )
