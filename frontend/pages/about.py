"""About page for CreditSetu AI."""

import streamlit as st

from components.cards import render_section_title


def render_about() -> None:
    """Render product and architecture overview."""
    render_section_title(
        "About CreditSetu AI",
        "A production-ready frontend architecture for responsible loan approval workflows.",
    )

    left, right = st.columns([1.1, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            """
#### Product Vision
CreditSetu AI is designed as a premium lending command center where bank teams can
prepare applications, review model insights, examine fairness signals, and maintain
clear operational history.
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            """
#### Architecture Principles
- UI modules contain presentation only
- Backend modules own future model orchestration
- Services isolate data and integration boundaries
- Utilities hold shared non-domain helpers
- Artifacts and models are separated from source code
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### Technology Stack")
    st.write("Python, Streamlit, Pandas, NumPy, Plotly, Scikit-learn, SHAP, Joblib")
    st.markdown("</div>", unsafe_allow_html=True)
