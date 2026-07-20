"""Fairness report loading service."""

import json
from pathlib import Path
from typing import Any

import pandas as pd

from backend.config import FAIRNESS_REPORT_PATH
from backend.logger import get_logger
from backend.schemas import FairnessReport


class FairnessService:
    """Load responsible lending fairness diagnostics."""

    def __init__(self, report_path: Path = FAIRNESS_REPORT_PATH) -> None:
        self.report_path = report_path
        self.logger = get_logger(__name__)

    def load_report(self) -> FairnessReport:
        """Load fairness report from JSON artifact or return defaults."""
        if not self.report_path.exists():
            self.logger.warning("Fairness report not found. Returning default report.")
            return self._default_report()

        try:
            data = json.loads(self.report_path.read_text(encoding="utf-8"))
            return FairnessReport(
                generated_at=str(data.get("generated_at", "Unavailable")),
                summary=dict(data.get("summary", {})),
                segments=list(data.get("segments", [])),
            )
        except Exception:
            self.logger.exception("Unable to load fairness report.")
            return self._default_report()

    def to_dataframe(self) -> pd.DataFrame:
        """Return fairness segments as a DataFrame."""
        report = self.load_report()
        return pd.DataFrame(report.segments)

    @staticmethod
    def _default_report() -> FairnessReport:
        """Return safe default fairness data."""
        return FairnessReport(
            generated_at="Static baseline",
            summary={
                "status": "Baseline",
                "message": "No trained fairness artifact has been generated yet.",
            },
            segments=[
                {
                    "segment": "Urban",
                    "approval_rate": 0.76,
                    "baseline_rate": 0.72,
                    "gap": 0.04,
                    "status": "Healthy",
                },
                {
                    "segment": "Semiurban",
                    "approval_rate": 0.71,
                    "baseline_rate": 0.72,
                    "gap": -0.01,
                    "status": "Healthy",
                },
                {
                    "segment": "Rural",
                    "approval_rate": 0.66,
                    "baseline_rate": 0.72,
                    "gap": -0.06,
                    "status": "Watch",
                },
                {
                    "segment": "New-to-Credit",
                    "approval_rate": 0.61,
                    "baseline_rate": 0.72,
                    "gap": -0.11,
                    "status": "Review",
                },
            ],
        )
