"""SHAP explanation generation."""

from typing import Any

import numpy as np

from backend.logger import get_logger
from backend.schemas import ShapExplanation


class ShapService:
    """Generate model explanations with SHAP when artifacts support it."""

    def __init__(self) -> None:
        self.logger = get_logger(__name__)
        self._explainer: Any | None = None
        self._explainer_model_id: int | None = None

    def explain(
        self,
        model: Any,
        processed_features: Any,
        feature_names: list[str],
        probability: float,
    ) -> ShapExplanation:
        """Return a SHAP explanation for one application."""
        try:
            explainer = self._get_explainer(model, processed_features)
            explanation = explainer(processed_features)
            values = np.asarray(explanation.values)

            if values.ndim == 3:
                values = values[0, :, -1]
            elif values.ndim == 2:
                values = values[0]
            else:
                values = values.reshape(-1)

            impacts = self._format_impacts(values, feature_names)
            base_value = self._extract_base_value(explanation)
            return ShapExplanation(
                available=True,
                base_value=base_value,
                final_value=probability,
                feature_impacts=impacts,
            )
        except Exception as exc:
            self.logger.warning("SHAP explanation unavailable: %s", exc)
            return ShapExplanation(
                available=False,
                base_value=None,
                final_value=probability,
                feature_impacts=[],
                message="SHAP explanation is unavailable for the current artifacts.",
            )

    def _get_explainer(self, model: Any, processed_features: Any) -> Any:
        """Return a cached SHAP explainer for the active model instance."""
        model_id = id(model)
        if self._explainer is None or self._explainer_model_id != model_id:
            import shap

            self._explainer = shap.Explainer(model, processed_features)
            self._explainer_model_id = model_id
        return self._explainer

    @staticmethod
    def _format_impacts(values: np.ndarray, feature_names: list[str]) -> list[dict[str, Any]]:
        """Format feature contribution values for UI and logs."""
        flattened = values.astype(float).reshape(-1)
        names = feature_names[: len(flattened)]
        if len(names) < len(flattened):
            names = names + [f"feature_{index}" for index in range(len(names), len(flattened))]

        impacts = [
            {"feature": name, "impact": float(value)}
            for name, value in zip(names, flattened)
        ]
        return sorted(impacts, key=lambda item: abs(item["impact"]), reverse=True)[:12]

    @staticmethod
    def _extract_base_value(explanation: Any) -> float | None:
        """Read SHAP base value from an explanation object."""
        base_values = getattr(explanation, "base_values", None)
        if base_values is None:
            return None
        values = np.asarray(base_values).reshape(-1)
        if values.size == 0:
            return None
        return float(values[-1])
