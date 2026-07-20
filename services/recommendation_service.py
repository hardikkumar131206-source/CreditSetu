"""Generate lender-facing recommendation cards."""

from backend.schemas import LoanApplication, RecommendationCard, ShapExplanation


class RecommendationService:
    """Create recommendations from application and prediction context."""

    def build_cards(
        self,
        application: LoanApplication,
        probability: float,
        shap_explanation: ShapExplanation | None,
    ) -> list[RecommendationCard]:
        """Return prioritized recommendation cards."""
        cards: list[RecommendationCard] = []

        if probability >= 0.75:
            cards.append(
                RecommendationCard(
                    title="Fast-track eligible",
                    message="Approval probability is strong. Route for standard documentation checks.",
                    tone="green",
                    priority=1,
                )
            )
        elif probability >= 0.5:
            cards.append(
                RecommendationCard(
                    title="Manual review recommended",
                    message="Score is positive but not decisive. Ask underwriting to review affordability.",
                    tone="purple",
                    priority=1,
                )
            )
        else:
            cards.append(
                RecommendationCard(
                    title="Risk mitigation required",
                    message="Approval probability is low. Consider lower exposure or stronger collateral.",
                    tone="pink",
                    priority=1,
                )
            )

        if application.dti_ratio > 45:
            cards.append(
                RecommendationCard(
                    title="High DTI pressure",
                    message="Debt-to-income ratio is elevated. Request income proof and liability details.",
                    tone="pink",
                    priority=2,
                )
            )
        if application.credit_score < 650:
            cards.append(
                RecommendationCard(
                    title="Credit score watch",
                    message="Credit score is below prime range. Review repayment history before sanctioning.",
                    tone="purple",
                    priority=3,
                )
            )
        if not application.has_coapplicant and application.loan_amount > application.annual_income:
            cards.append(
                RecommendationCard(
                    title="Add support strength",
                    message="Loan amount exceeds annual income. A co-applicant can improve affordability.",
                    tone="blue",
                    priority=4,
                )
            )
        if shap_explanation and shap_explanation.available:
            top_driver = max(
                shap_explanation.feature_impacts,
                key=lambda item: abs(float(item.get("impact", 0))),
                default=None,
            )
            if top_driver:
                cards.append(
                    RecommendationCard(
                        title="Top model driver",
                        message=f"{top_driver['feature']} is the strongest scoring influence.",
                        tone="blue",
                        priority=5,
                    )
                )

        return sorted(cards, key=lambda card: card.priority)
