"""Loan prediction page containing applicant intake controls."""

import pandas as pd
import streamlit as st

from components.cards import render_recommendation_card, render_section_title
from components.visuals import render_feature_impact
from frontend.dependencies import get_services


def render_loan_prediction() -> None:
    """Render the loan prediction input experience."""
    services = get_services()
    render_section_title(
        "Loan Prediction Studio",
        "Capture applicant details and prepare a request for the backend scoring service.",
    )

    with st.form("loan_prediction_form", clear_on_submit=False):
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Applicant Profile")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            applicant_id = st.text_input(
                "Applicant ID",
                placeholder="CS-APP-1024",
                help="Optional. A secure ID is generated when left blank.",
                key="applicant_id",
            )
            annual_income = st.number_input(
                "Annual Income",
                min_value=0,
                step=5000,
                help="Gross annual income before taxes.",
                key="annual_income",
            )
            employment_type = st.selectbox(
                "Employment Type",
                ["Salaried", "Self-employed", "Business Owner", "Contract"],
                key="employment_type",
            )
        with col_b:
            loan_amount = st.number_input(
                "Loan Amount",
                min_value=0,
                step=2500,
                key="loan_amount",
            )
            loan_term = st.number_input(
                "Loan Term (months)",
                min_value=6,
                max_value=360,
                key="loan_term",
            )
            property_area = st.selectbox(
                "Property Area",
                ["Urban", "Semiurban", "Rural"],
                key="property_area",
            )
        with col_c:
            credit_score = st.slider("Credit Score", 300, 900, 720, key="credit_score")
            dti_ratio = st.slider("Debt-to-Income Ratio", 0, 100, 32, key="dti_ratio")
            education = st.selectbox(
                "Education",
                ["Graduate", "Post Graduate", "Professional", "Other"],
                key="education",
            )
        st.markdown("</div>", unsafe_allow_html=True)

        left, right = st.columns([1.2, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("#### Co-Applicant & Collateral")
            has_coapplicant = st.toggle("Co-applicant available", key="has_coapplicant")
            co_income = st.number_input(
                "Co-applicant Income",
                min_value=0,
                step=2500,
                key="co_income",
            )
            collateral_type = st.selectbox(
                "Collateral Type",
                ["Residential Property", "Commercial Property", "Vehicle", "None"],
                key="collateral_type",
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel callout-panel">', unsafe_allow_html=True)
            st.markdown("#### Scoring Status")
            st.info("Submit the application to the backend scoring service.")
            submitted = st.form_submit_button("Predict Approval", type="primary")
            st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        payload = _build_payload(
            applicant_id,
            annual_income,
            employment_type,
            loan_amount,
            loan_term,
            property_area,
            credit_score,
            dti_ratio,
            education,
            has_coapplicant,
            co_income,
            collateral_type,
        )
        with st.spinner("Scoring application and preparing explanations..."):
            result = services.prediction_service.predict(payload)
        _render_prediction_result(result)


def _build_payload(
    applicant_id,
    annual_income,
    employment_type,
    loan_amount,
    loan_term,
    property_area,
    credit_score,
    dti_ratio,
    education,
    has_coapplicant,
    co_income,
    collateral_type,
) -> dict:
    """Build a backend request payload from validated widget values."""
    return {
        "applicant_id": applicant_id,
        "annual_income": annual_income,
        "employment_type": employment_type,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "property_area": property_area,
        "credit_score": credit_score,
        "dti_ratio": dti_ratio,
        "education": education,
        "has_coapplicant": has_coapplicant,
        "co_income": co_income,
        "collateral_type": collateral_type,
    }


def _render_prediction_result(result) -> None:
    """Render backend prediction response."""
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### Prediction Result")
    if not result.success:
        st.error("Prediction could not be completed.")
        for error in result.errors:
            st.warning(error)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    metric_cols = st.columns(4)
    metric_cols[0].metric("Decision", result.prediction)
    metric_cols[1].metric("Probability", f"{result.probability:.1%}")
    metric_cols[2].metric("Confidence", result.confidence)
    metric_cols[3].metric("Application", result.application_id)
    st.markdown("</div>", unsafe_allow_html=True)

    rec_col, shap_col = st.columns([1, 1.2])
    with rec_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Recommendation Cards")
        if result.recommendations:
            for card in result.recommendations:
                render_recommendation_card(card.title, card.message, card.tone)
        else:
            st.info("No recommendations were generated for this application.")
        st.markdown("</div>", unsafe_allow_html=True)

    with shap_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### SHAP Explanation")
        explanation = result.shap_explanation
        if explanation and explanation.available:
            render_feature_impact(pd.DataFrame(explanation.feature_impacts))
        elif explanation and explanation.message:
            st.info(explanation.message)
        else:
            st.info("No explanation is available for this prediction.")
        st.markdown("</div>", unsafe_allow_html=True)
