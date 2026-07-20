"""Dependency injection container for application services."""

from dataclasses import dataclass

from services.fairness_service import FairnessService
from services.history_service import HistoryService
from services.model_service import ModelService
from services.prediction_service import PredictionService
from services.preprocessing_service import PreprocessingService
from services.recommendation_service import RecommendationService
from services.shap_service import ShapService


@dataclass(frozen=True)
class ServiceContainer:
    """Container holding application service dependencies."""

    model_service: ModelService
    preprocessing_service: PreprocessingService
    shap_service: ShapService
    recommendation_service: RecommendationService
    history_service: HistoryService
    fairness_service: FairnessService
    prediction_service: PredictionService


def build_service_container() -> ServiceContainer:
    """Build service dependencies with explicit injection."""
    model_service = ModelService()
    preprocessing_service = PreprocessingService()
    shap_service = ShapService()
    recommendation_service = RecommendationService()
    history_service = HistoryService()
    fairness_service = FairnessService()
    prediction_service = PredictionService(
        model_service=model_service,
        preprocessing_service=preprocessing_service,
        shap_service=shap_service,
        recommendation_service=recommendation_service,
        history_service=history_service,
    )
    return ServiceContainer(
        model_service=model_service,
        preprocessing_service=preprocessing_service,
        shap_service=shap_service,
        recommendation_service=recommendation_service,
        history_service=history_service,
        fairness_service=fairness_service,
        prediction_service=prediction_service,
    )
