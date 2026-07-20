"""Model artifact loading and inference helpers."""

from pathlib import Path
from typing import Any

import joblib
import numpy as np

from backend.config import MODEL_PATH
from backend.exceptions import ArtifactLoadError, PredictionError
from backend.logger import get_logger


class ModelService:
    """Load and execute the trained approval model."""

    def __init__(self, model_path: Path = MODEL_PATH) -> None:
        self.model_path = model_path
        self._model: Any | None = None
        self.logger = get_logger(__name__)

    @property
    def model(self) -> Any:
        """Return the loaded model."""
        if self._model is None:
            self._model = self._load_model()
        return self._model

    def predict(self, features: Any) -> tuple[str, float]:
        """Return approval decision and positive-class probability."""
        try:
            model = self.model
            probability = self._positive_probability(model, features)
            if probability is not None:
                label = self._prediction_from_probability(probability)
                return label, probability

            raw_prediction = model.predict(features)[0]
            prediction = self._normalize_prediction(raw_prediction)
            probability = 1.0 if prediction == "Approved" else 0.0
            return prediction, probability
        except ArtifactLoadError:
            raise
        except Exception as exc:
            self.logger.exception("Model prediction failed.")
            raise PredictionError("Model prediction failed.") from exc

    def _load_model(self) -> Any:
        """Load model artifact from disk using Joblib."""
        if not self.model_path.exists():
            raise ArtifactLoadError(
                "The trained model artifact is missing. Add model.joblib to "
                "the artifacts directory before running predictions."
            )
        try:
            self.logger.info("Loading model artifact: %s", self.model_path)
            return joblib.load(self.model_path)
        except Exception as exc:
            self.logger.exception("Unable to load model artifact.")
            raise ArtifactLoadError("Unable to load trained model artifact.") from exc

    @staticmethod
    def _positive_probability(model: Any, features: Any) -> float | None:
        """Read positive class probability when the model supports it."""
        if not hasattr(model, "predict_proba"):
            return None

        probabilities = np.asarray(model.predict_proba(features))
        if probabilities.ndim != 2:
            return None

        positive_index = 1 if probabilities.shape[1] > 1 else 0
        classes = getattr(model, "classes_", None)
        if classes is not None:
            normalized = [ModelService._normalize_prediction(item) for item in classes]
            if "Approved" in normalized:
                positive_index = normalized.index("Approved")

        return float(probabilities[0, positive_index])

    @staticmethod
    def _prediction_from_probability(probability: float) -> str:
        """Convert probability into an approval label."""
        return "Approved" if probability >= 0.5 else "Declined"

    @staticmethod
    def _normalize_prediction(value: Any) -> str:
        """Normalize model output labels."""
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"approved", "approve", "yes", "y", "1", "true"}:
                return "Approved"
            if lowered in {"declined", "decline", "no", "n", "0", "false"}:
                return "Declined"
        try:
            return "Approved" if int(value) == 1 else "Declined"
        except (TypeError, ValueError):
            return "Approved" if bool(value) else "Declined"
