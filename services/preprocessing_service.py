"""Preprocessing pipeline loading and feature transformation."""

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from backend.config import FEATURE_COLUMNS, PREPROCESSOR_PATH
from backend.exceptions import ArtifactLoadError
from backend.logger import get_logger
from backend.schemas import LoanApplication


class PreprocessingService:
    """Load and apply the preprocessing pipeline."""

    def __init__(
        self,
        preprocessor_path: Path = PREPROCESSOR_PATH,
        feature_columns: list[str] | None = None,
    ) -> None:
        self.preprocessor_path = preprocessor_path
        self.feature_columns = feature_columns or FEATURE_COLUMNS
        self._preprocessor: Any | None = None
        self.logger = get_logger(__name__)

    @property
    def preprocessor(self) -> Any:
        """Return the loaded preprocessing pipeline."""
        if self._preprocessor is None:
            self._preprocessor = self._load_preprocessor()
        return self._preprocessor

    def to_dataframe(self, application: LoanApplication) -> pd.DataFrame:
        """Convert a validated application into ordered raw features."""
        return pd.DataFrame([application.to_features()], columns=self.feature_columns)

    def transform(self, application: LoanApplication) -> Any:
        """Preprocess validated application features."""
        raw_features = self.to_dataframe(application)
        try:
            return self.preprocessor.transform(raw_features)
        except ArtifactLoadError:
            raise
        except Exception as exc:
            self.logger.exception("Feature preprocessing failed.")
            raise ArtifactLoadError("Feature preprocessing failed.") from exc

    def get_feature_names(self) -> list[str]:
        """Return transformed feature names when available."""
        preprocessor = self.preprocessor
        if hasattr(preprocessor, "get_feature_names_out"):
            return [str(name) for name in preprocessor.get_feature_names_out()]
        return self.feature_columns

    def _load_preprocessor(self) -> Any:
        """Load preprocessing pipeline from disk using Joblib."""
        if not self.preprocessor_path.exists():
            raise ArtifactLoadError(
                "The preprocessing pipeline artifact is missing. Add "
                "preprocessing_pipeline.joblib to the artifacts directory "
                "before running predictions."
            )
        try:
            self.logger.info("Loading preprocessing artifact: %s", self.preprocessor_path)
            return joblib.load(self.preprocessor_path)
        except Exception as exc:
            self.logger.exception("Unable to load preprocessing artifact.")
            raise ArtifactLoadError("Unable to load preprocessing pipeline.") from exc
