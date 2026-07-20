"""Fairness analysis page for future responsible lending diagnostics."""

import streamlit as st

from components.cards import render_section_title
from components.visuals import render_fairness_gap, render_segment_approval
from frontend.dependencies import get_services


def render_fairness() -> None:
    """Render fairness monitoring UI surfaces."""
    services = get_services()
    report = services.fairness_service.load_report()
    fairness = services.fairness_service.to_dataframe()
    render_section_title(
        "Fairness Analysis",
        "Monitor approval parity, segment drift, and responsible lending indicators.",
    )

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### Fairness Report Status")
    st.write(report.summary.get("message", "Fairness report loaded."))
    st.caption(f"Generated at: {report.generated_at}")
    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Segment Approval Rates")
        with st.spinner("Loading approval parity chart..."):
            render_segment_approval(fairness)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Fairness Gap")
        with st.spinner("Loading fairness gap chart..."):
            render_fairness_gap(fairness)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel table-panel">', unsafe_allow_html=True)
    st.markdown("#### Governance Checklist")
    if fairness.empty:
        st.info("No fairness segment data is available.")
    else:
        st.dataframe(
            fairness[["segment", "approval_rate", "baseline_rate", "gap", "status"]],
            use_container_width=True,
            hide_index=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
