"""Frontend access point for backend service dependencies."""

import streamlit as st

from services.container import ServiceContainer, build_service_container


@st.cache_resource
def get_services() -> ServiceContainer:
    """Return cached backend service dependencies."""
    return build_service_container()
