"""SHAP explainability page."""

import streamlit as st
import pandas as pd

from components.cards import render_section_title
from components.visuals import render_feature_impact
from frontend.dependencies import get_services


def render_shap_explainability() -> None:
    """Render model explainability surfaces without model execution."""
    impacts = get_services().history_service.latest_shap_impacts()
    impact_data = pd.DataFrame(impacts)
    render_section_title(
        "SHAP Explainability",
        "Interpretability workspace for model-level feature attribution.",
    )

    top, side = st.columns([1.35, 1])
    with top:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Latest Feature Impact")
        with st.spinner("Loading latest explanation..."):
            render_feature_impact(impact_data)
        st.markdown("</div>", unsafe_allow_html=True)
    with side:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Explanation Summary")
        st.metric("Tracked Features", str(len(impacts)))
        st.metric("Available Runs", "1" if impacts else "0")
        st.metric("Backend Source", "History")
        st.caption("Run a successful prediction to populate SHAP impacts.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### Attribution Controls")
    left, middle, right = st.columns(3)
    with left:
        st.selectbox("Application", ["CS-APP-1024", "CS-APP-1025", "CS-APP-1026"])
    with middle:
        st.selectbox("Explanation Type", ["Local", "Global", "Cohort"])
    with right:
        st.selectbox("Output View", ["Waterfall", "Beeswarm", "Decision Plot"])
    st.markdown("</div>", unsafe_allow_html=True)
