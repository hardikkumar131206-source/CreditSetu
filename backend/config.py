"""Application configuration and shared backend constants."""

from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
LOGS_DIR = ROOT_DIR / "logs"

MODEL_PATH = ARTIFACTS_DIR / "model.joblib"
PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessing_pipeline.joblib"
FAIRNESS_REPORT_PATH = ARTIFACTS_DIR / "fairness_report.json"
APPLICATION_HISTORY_PATH = LOGS_DIR / "application_history.jsonl"
APP_LOG_PATH = LOGS_DIR / "creditsetu.log"

FEATURE_COLUMNS = [
    "annual_income",
    "employment_type",
    "loan_amount",
    "loan_term",
    "property_area",
    "credit_score",
    "dti_ratio",
    "education",
    "has_coapplicant",
    "co_income",
    "collateral_type",
]


@dataclass(frozen=True)
class PredictionThresholds:
    """Decision thresholds used after model scoring."""

    approval: float = 0.6
    review: float = 0.45
    high_confidence: float = 0.75
    medium_confidence: float = 0.55
