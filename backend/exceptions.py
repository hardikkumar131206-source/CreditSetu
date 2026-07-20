"""Backend exception types."""


class CreditSetuError(Exception):
    """Base exception for backend failures."""


class ValidationError(CreditSetuError):
    """Raised when submitted application data is invalid."""


class ArtifactLoadError(CreditSetuError):
    """Raised when a required ML artifact cannot be loaded."""


class PredictionError(CreditSetuError):
    """Raised when model prediction fails."""
