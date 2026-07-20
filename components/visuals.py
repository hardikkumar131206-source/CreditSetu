"""Plotly visualization components."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


CHART_TEMPLATE = "plotly_dark"
GRID_COLOR = "rgba(148, 163, 184, 0.14)"
PAPER_COLOR = "rgba(0, 0, 0, 0)"
CHART_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}


def _apply_layout(fig: go.Figure) -> go.Figure:
    """Apply the application chart theme."""
    fig.update_layout(
        template=CHART_TEMPLATE,
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=PAPER_COLOR,
        margin=dict(l=12, r=12, t=18, b=12),
        font=dict(color="#d8e3f8", family="Inter, sans-serif"),
        hoverlabel=dict(bgcolor="#111827", bordercolor="#334155", font_size=13),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        autosize=True,
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig


def render_approval_trend(data) -> None:
    """Render monthly approval trend chart."""
    if data.empty:
        st.info("No approval trend data is available.")
        return

    fig = px.area(
        data,
        x="month",
        y="approval_rate",
        color_discrete_sequence=["#4f8cff"],
    )
    fig.update_traces(line=dict(width=3), fill="tozeroy")
    fig.update_yaxes(ticksuffix="%")
    st.plotly_chart(_apply_layout(fig), use_container_width=True, config=CHART_CONFIG)


def render_risk_mix(data) -> None:
    """Render risk band distribution chart."""
    if data.empty:
        st.info("No risk composition data is available.")
        return

    fig = px.pie(
        data,
        names="risk_band",
        values="loan_amount",
        hole=0.62,
        color="risk_band",
        color_discrete_map={"Low": "#3ddc97", "Medium": "#7c6cff", "High": "#ff6b8a"},
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(_apply_layout(fig), use_container_width=True, config=CHART_CONFIG)


def render_feature_impact(data) -> None:
    """Render future SHAP-style feature impact chart."""
    if data.empty:
        st.info("No explanation data is available yet.")
        return

    fig = px.bar(
        data,
        x="impact",
        y="feature",
        orientation="h",
        color="impact",
        color_continuous_scale=["#ff6b8a", "#7c6cff", "#3ddc97"],
    )
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(_apply_layout(fig), use_container_width=True, config=CHART_CONFIG)


def render_segment_approval(data) -> None:
    """Render segment approval comparison."""
    if data.empty:
        st.info("No segment approval data is available.")
        return

    fig = px.bar(
        data,
        x="segment",
        y=["approval_rate", "baseline_rate"],
        barmode="group",
        color_discrete_sequence=["#4f8cff", "#9b7cff"],
    )
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(_apply_layout(fig), use_container_width=True, config=CHART_CONFIG)


def render_fairness_gap(data) -> None:
    """Render fairness gap by segment."""
    if data.empty:
        st.info("No fairness gap data is available.")
        return

    fig = px.line(
        data,
        x="segment",
        y="gap",
        markers=True,
        color_discrete_sequence=["#ff6b8a"],
    )
    fig.add_hline(y=0, line_dash="dot", line_color="#94a3b8")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(_apply_layout(fig), use_container_width=True, config=CHART_CONFIG)
