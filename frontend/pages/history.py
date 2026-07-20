"""Application history page."""

import streamlit as st

from components.cards import render_section_title
from frontend.dependencies import get_services


def render_history() -> None:
    """Render application history management UI."""
    history = get_services().history_service.read_history()
    render_section_title(
        "Application History",
        "Track submitted applications, operational status, and audit readiness.",
    )

    filters = st.columns([1, 1.4])
    with filters[0]:
        status_filter = st.selectbox(
            "Prediction",
            ["All", "Approved", "Review", "Declined", "Unavailable"],
            key="status_filter",
        )
    with filters[1]:
        search = st.text_input(
            "Search",
            placeholder="Application ID or error text",
            key="history_search",
        )

    st.markdown('<div class="panel table-panel">', unsafe_allow_html=True)
    filtered_history = _filter_history(history, status_filter, search)
    if filtered_history.empty:
        message = (
            "No applications have been logged yet."
            if history.empty
            else "No logged applications match the selected filters."
        )
        st.info(message)
    else:
        st.dataframe(filtered_history, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _filter_history(history, status_filter: str, search: str):
    """Apply frontend table filters."""
    if history.empty:
        return history

    filtered = history.copy()
    if status_filter != "All":
        filtered = filtered[filtered["Prediction"] == status_filter]

    query = search.strip().lower()
    if query:
        searchable = (
            filtered["Application ID"].fillna("").astype(str)
            + " "
            + filtered["Errors"].fillna("").astype(str)
        ).str.lower()
        filtered = filtered[searchable.str.contains(query, regex=False)]
    return filtered
