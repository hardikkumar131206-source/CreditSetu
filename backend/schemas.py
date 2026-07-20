"""Typed backend data contracts."""

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    """Return a stable UTC timestamp for persisted records."""
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class LoanApplication:
    """Validated loan application request."""

    applicant_id: str
    annual_income: float
    employment_type: str
    loan_amount: float
    loan_term: int
    property_area: str
    credit_score: int
    dti_ratio: float
    education: str
    has_coapplicant: bool
    co_income: float
    collateral_type: str
    submitted_at: str = field(default_factory=utc_now_iso)

    @classmethod
    def with_generated_id(cls, **values: Any) -> "LoanApplication":
        """Create an application and generate an ID when missing."""
        values["applicant_id"] = values.get("applicant_id") or f"CS-{uuid4().hex[:10].upper()}"
        return cls(**values)

    def to_features(self) -> dict[str, Any]:
        """Return model feature values only."""
        values = asdict(self)
        values.pop("submitted_at")
        values.pop("applicant_id")
        return values

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        return asdict(self)


@dataclass(frozen=True)
class RecommendationCard:
    """Actionable recommendation surfaced after prediction."""

    title: str
    message: str
    tone: str
    priority: int

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        return asdict(self)


@dataclass(frozen=True)
class ShapExplanation:
    """SHAP explanation payload."""

    available: bool
    base_value: float | None
    final_value: float | None
    feature_impacts: list[dict[str, Any]]
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        return asdict(self)


@dataclass(frozen=True)
class PredictionResult:
    """Prediction response returned to callers."""

    success: bool
    application_id: str | None
    prediction: str | None
    probability: float | None
    confidence: str | None
    recommendations: list[RecommendationCard]
    shap_explanation: ShapExplanation | None
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        values = asdict(self)
        values["recommendations"] = [card.to_dict() for card in self.recommendations]
        if self.shap_explanation:
            values["shap_explanation"] = self.shap_explanation.to_dict()
        return values


@dataclass(frozen=True)
class FairnessReport:
    """Loaded fairness report contract."""

    generated_at: str
    summary: dict[str, Any]
    segments: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        return asdict(self)
