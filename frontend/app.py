"""Streamlit application shell for CreditSetu AI."""

from pathlib import Path

import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar
from frontend.pages.about import render_about
from frontend.pages.dashboard import render_dashboard
from frontend.pages.fairness import render_fairness
from frontend.pages.history import render_history
from frontend.pages.loan_prediction import render_loan_prediction
from frontend.pages.shap_explainability import render_shap_explainability


PAGE_RENDERERS = {
    "Dashboard": render_dashboard,
    "Loan Prediction": render_loan_prediction,
    "SHAP Explainability": render_shap_explainability,
    "Fairness Analysis": render_fairness,
    "Application History": render_history,
    "About": render_about,
}


def load_css() -> None:
    """Load the single application stylesheet."""
    css_path = Path(__file__).parent / "styles" / "theme.css"
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


def main() -> None:
    """Render the CreditSetu AI frontend."""
    st.set_page_config(
        page_title="CreditSetu AI",
        page_icon="assets/logo.svg",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    load_css()

    selected_page = render_sidebar(list(PAGE_RENDERERS.keys()))
    render_header(selected_page)
    PAGE_RENDERERS[selected_page]()


if __name__ == "__main__":
    main()
