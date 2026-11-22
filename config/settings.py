import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
MODULES_DIR = BASE_DIR / "modules"
PAGES_DIR = BASE_DIR / "pages"
DATASET_DIR = BASE_DIR / "dataset"
MODELS_DIR = BASE_DIR / "models"
DATABASE_DIR = BASE_DIR / "database"
OUTPUT_DIR = BASE_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
SAMPLE_CODE_DIR = BASE_DIR / "sample_code"

# Ensure runtime directories exist
for directory in [DATASET_DIR, MODELS_DIR, DATABASE_DIR, OUTPUT_DIR, REPORTS_DIR, SAMPLE_CODE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database Configuration
DATABASE_PATH = DATABASE_DIR / "analysis_history.db"

# Risk Thresholds (Configurable bands)
DEFAULT_LOW_RISK_THRESHOLD = 0.30   # Probability < 0.30 -> Low Risk
DEFAULT_HIGH_RISK_THRESHOLD = 0.70  # Probability > 0.70 -> High Risk
# Probability between 0.30 and 0.70 -> Medium Risk

# Metric Heuristic Thresholds (Software Engineering Standards)
METRIC_THRESHOLDS = {
    "loc": {"warning": 30, "critical": 60},
    "cyclomatic_complexity": {"warning": 8, "critical": 15},
    "max_nesting_depth": {"warning": 3, "critical": 5},
    "param_count": {"warning": 4, "critical": 7},
    "return_count": {"warning": 3, "critical": 6},
    "loop_count": {"warning": 3, "critical": 5},
    "condition_count": {"warning": 4, "critical": 8},
    "call_count": {"warning": 6, "critical": 12},
    "exception_count": {"warning": 2, "critical": 5},
}

# Machine Learning Configuration
PRIMARY_MODEL_FILE = MODELS_DIR / "defect_predictor_rf.joblib"
SCALER_FILE = MODELS_DIR / "feature_scaler.joblib"
METRIC_COLUMNS_FILE = MODELS_DIR / "feature_columns.joblib"
MODEL_METRICS_FILE = MODELS_DIR / "model_evaluation_metrics.json"

# Supported Input Constraints
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB
MAX_SOURCE_LINES = 5000
SUPPORTED_EXTENSIONS = [".py"]
