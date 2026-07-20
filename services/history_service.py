"""Application history persistence."""

import json
from pathlib import Path
from typing import Any

import pandas as pd

from backend.config import APPLICATION_HISTORY_PATH, LOGS_DIR
from backend.logger import get_logger
from backend.schemas import LoanApplication, PredictionResult, utc_now_iso


class HistoryService:
    """Append and read application history records."""

    def __init__(self, history_path: Path = APPLICATION_HISTORY_PATH) -> None:
        self.history_path = history_path
        self.logger = get_logger(__name__)
        LOGS_DIR.mkdir(exist_ok=True)

    def log_application(
        self,
        application: LoanApplication | None,
        result: PredictionResult,
        raw_input: dict[str, Any] | None = None,
    ) -> None:
        """Persist one application attempt."""
        try:
            record = {
                "logged_at": utc_now_iso(),
                "application": application.to_dict() if application else raw_input or {},
                "result": result.to_dict(),
            }
            with self.history_path.open("a", encoding="utf-8") as history_file:
                history_file.write(json.dumps(record, default=str) + "\n")
        except Exception:
            self.logger.exception("Unable to persist application history.")

    def read_history(self) -> pd.DataFrame:
        """Read persisted application history as a display-ready DataFrame."""
        records = self.read_records()

        rows = [self._flatten_record(record) for record in records]
        return pd.DataFrame(rows) if rows else self._empty_history()

    def read_records(self) -> list[dict[str, Any]]:
        """Read raw persisted application records."""
        if not self.history_path.exists():
            return []

        records: list[dict[str, Any]] = []
        try:
            with self.history_path.open("r", encoding="utf-8") as history_file:
                for line in history_file:
                    if line.strip():
                        records.append(json.loads(line))
        except Exception:
            self.logger.exception("Unable to read application history.")
            return []
        return records

    def latest_shap_impacts(self) -> list[dict[str, Any]]:
        """Return latest available SHAP impacts from history."""
        for record in reversed(self.read_records()):
            explanation = record.get("result", {}).get("shap_explanation") or {}
            impacts = explanation.get("feature_impacts") or []
            if explanation.get("available") and impacts:
                return impacts
        return []

    @staticmethod
    def _flatten_record(record: dict[str, Any]) -> dict[str, Any]:
        """Flatten stored JSON into table columns."""
        application = record.get("application", {})
        result = record.get("result", {})
        probability = result.get("probability")
        return {
            "Logged At": record.get("logged_at"),
            "Application ID": result.get("application_id") or application.get("applicant_id"),
            "Loan Amount": application.get("loan_amount"),
            "Annual Income": application.get("annual_income"),
            "Prediction": result.get("prediction") or "Unavailable",
            "Probability": f"{probability:.1%}" if isinstance(probability, float) else "",
            "Confidence": result.get("confidence") or "Unavailable",
            "Errors": "; ".join(result.get("errors", [])),
        }

    @staticmethod
    def _empty_history() -> pd.DataFrame:
        """Return a correctly shaped empty history table."""
        return pd.DataFrame(
            columns=[
                "Logged At",
                "Application ID",
                "Loan Amount",
                "Annual Income",
                "Prediction",
                "Probability",
                "Confidence",
                "Errors",
            ]
        )
