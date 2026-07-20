# CreditSetu AI

CreditSetu AI is a Streamlit loan approval prediction dashboard with a separated frontend and service-backed ML orchestration layer.

## Run

```powershell
streamlit run app.py
```

## Required Artifacts

Place trained artifacts in `artifacts/`:

- `model.joblib`
- `preprocessing_pipeline.joblib`
- `fairness_report.json`

The application fails gracefully when model artifacts are missing. Prediction attempts and backend logs are written under `logs/`, which is ignored by Git.

## Architecture

- `frontend/`: Streamlit pages and dependency access
- `components/`: reusable UI components and Plotly visualizations
- `services/`: model loading, preprocessing, prediction orchestration, SHAP, fairness, recommendations, and history
- `backend/`: configuration, schemas, validation, exceptions, and logging
- `artifacts/`: trained model assets and fairness report
