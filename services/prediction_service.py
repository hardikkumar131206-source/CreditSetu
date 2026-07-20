"""Loan prediction orchestration service."""

from typing import Any

from backend.config import PredictionThresholds
from backend.exceptions import ArtifactLoadError, CreditSetuError, ValidationError
from backend.logger import get_logger
from backend.schemas import PredictionResult, ShapExplanation
from backend.validators import validate_application
from services.history_service import HistoryService
from services.model_service import ModelService
from services.preprocessing_service import PreprocessingService
from services.recommendation_service import RecommendationService
from services.shap_service import ShapService


class PredictionService:
    """Validate, preprocess, score, explain, recommend, and log applications."""

    def __init__(
        self,
        model_service: ModelService,
        preprocessing_service: PreprocessingService,
        shap_service: ShapService,
        recommendation_service: RecommendationService,
        history_service: HistoryService,
        thresholds: PredictionThresholds | None = None,
    ) -> None:
        self.model_service = model_service
        self.preprocessing_service = preprocessing_service
        self.shap_service = shap_service
        self.recommendation_service = recommendation_service
        self.history_service = history_service
        self.thresholds = thresholds or PredictionThresholds()
        self.logger = get_logger(__name__)

    def predict(self, raw_input: dict[str, Any]) -> PredictionResult:
        """Return a full prediction response and never raise to callers."""
        raw_input = raw_input or {}
        application = None
        try:
            application = validate_application(raw_input)
            processed_features = self.preprocessing_service.transform(application)
            prediction, probability = self.model_service.predict(processed_features)
            decision = self._decision_label(prediction, probability)
            confidence = self._confidence_label(probability)

            shap_explanation = self.shap_service.explain(
                self.model_service.model,
                processed_features,
                self.preprocessing_service.get_feature_names(),
                probability,
            )
            recommendations = self.recommendation_service.build_cards(
                application,
                probability,
                shap_explanation,
            )
            result = PredictionResult(
                success=True,
                application_id=application.applicant_id,
                prediction=decision,
                probability=round(probability, 4),
                confidence=confidence,
                recommendations=recommendations,
                shap_explanation=shap_explanation,
            )
            self.logger.info(
                "Prediction completed for %s with result=%s probability=%.4f",
                application.applicant_id,
                decision,
                probability,
            )
        except ValidationError as exc:
            self.logger.info("Validation failed: %s", exc)
            result = self._failure_result([str(exc)], raw_input.get("applicant_id"))
        except ArtifactLoadError as exc:
            self.logger.error("Artifact unavailable: %s", exc)
            result = self._failure_result([str(exc)], raw_input.get("applicant_id"))
        except CreditSetuError as exc:
            self.logger.exception("Prediction service failed.")
            result = self._failure_result([str(exc)], raw_input.get("applicant_id"))
        except Exception:
            self.logger.exception("Unexpected prediction service failure.")
            result = self._failure_result(
                ["Unexpected backend error. Please check logs for details."],
                raw_input.get("applicant_id"),
            )

        self.history_service.log_application(application, result, raw_input)
        return result

    def _decision_label(self, prediction: str, probability: float) -> str:
        """Map model output and probability into business decision labels."""
        if probability >= self.thresholds.approval:
            return "Approved"
        if probability >= self.thresholds.review:
            return "Review"
        return "Declined" if prediction == "Declined" else "Review"

    def _confidence_label(self, probability: float) -> str:
        """Return a confidence band."""
        certainty = max(probability, 1 - probability)
        if certainty >= self.thresholds.high_confidence:
            return "High"
        if certainty >= self.thresholds.medium_confidence:
            return "Medium"
        return "Low"

    @staticmethod
    def _failure_result(errors: list[str], application_id: Any) -> PredictionResult:
        """Build a safe failure response."""
        return PredictionResult(
            success=False,
            application_id=str(application_id).strip() or None,
            prediction=None,
            probability=None,
            confidence=None,
            recommendations=[],
            shap_explanation=ShapExplanation(
                available=False,
                base_value=None,
                final_value=None,
                feature_impacts=[],
                message="Explanation unavailable because prediction did not complete.",
            ),
            errors=errors,
        )
