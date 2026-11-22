"""
Data Loader module for Software Defect Prediction datasets.
Loads, cleans, validates, and preprocesses legitimate NASA PROMISE defect datasets (e.g., KC1, JM1, CM1).
"""

import os
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional
import pandas as pd
import numpy as np

from config.settings import DATASET_DIR


class DefectDataLoader:
    """Manages loading and preprocessing of software defect datasets."""

    TARGET_COLUMN_CANDIDATES = ["defects", "defective", "problems", "bug", "label", "class"]

    # Mapping of NASA metric names to standardized feature names
    METRIC_RENAME_MAP = {
        "v(g)": "cyclomatic_complexity",
        "ev(g)": "essential_complexity",
        "iv(g)": "design_complexity",
        "l": "h_length_level",
        "v": "h_volume",
        "d": "h_difficulty",
        "i": "h_intelligence",
        "e": "h_effort",
        "b": "h_bugs",
        "t": "h_time",
        "n": "h_length",
        "locode": "loc_code",
        "locomment": "loc_comment",
        "loblank": "loc_blank",
        "loccodeandcomment": "loc_code_comment",
        "uniq_op": "uniq_op",
        "uniq_opnd": "uniq_opnd",
        "total_op": "total_op",
        "total_opnd": "total_opnd",
        "branchcount": "branch_count",
    }

    @classmethod
    def get_available_datasets(cls) -> List[str]:
        """Returns names of CSV files found in the dataset directory."""
        if not DATASET_DIR.exists():
            return []
        return [f.name for f in DATASET_DIR.glob("*.csv")]

    @classmethod
    def load_dataset(
        cls,
        dataset_name_or_path: Optional[str] = None,
        prefer_openml_id: Optional[int] = 1067,  # Default: NASA KC1 (OpenML id 1067)
    ) -> Tuple[pd.DataFrame, pd.Series, List[str], Dict[str, Any]]:
        """
        Loads and cleans a defect prediction dataset.
        Returns:
            X (features DataFrame),
            y (binary defect labels Series),
            feature_names (list of string feature column names),
            metadata (dictionary with dataset statistics)
        """
        df: Optional[pd.DataFrame] = None
        source_desc = ""

        # 1. Attempt to load from specified path or default directory
        if dataset_name_or_path:
            target_path = Path(dataset_name_or_path)
            if not target_path.is_absolute():
                target_path = DATASET_DIR / target_path
            if target_path.exists():
                df = pd.read_csv(target_path)
                source_desc = f"Local file: {target_path.name}"
            else:
                raise FileNotFoundError(
                    f"Specified dataset file '{dataset_name_or_path}' was not found at '{target_path}'. "
                    "Please verify the filename or provide a valid CSV file."
                )

        # 2. If no path given, check if any CSV exists in dataset/
        if df is None:
            csv_files = list(DATASET_DIR.glob("*.csv"))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                source_desc = f"Local file: {csv_files[0].name}"

        # 3. If still None, try fetching from OpenML
        if df is None and prefer_openml_id is not None:
            try:
                from sklearn.datasets import fetch_openml
                print(f"Fetching NASA dataset (OpenML ID: {prefer_openml_id})...")
                openml_data = fetch_openml(data_id=prefer_openml_id, as_frame=True, parser="auto")
                df = openml_data.frame
                source_desc = f"OpenML NASA Dataset (ID: {prefer_openml_id})"
                # Cache locally for offline execution
                local_cache_path = DATASET_DIR / f"nasa_openml_{prefer_openml_id}.csv"
                df.to_csv(local_cache_path, index=False)
            except Exception as e:
                print(f"OpenML download unavailable: {e}")

        # 4. If still None, raise error with explicit instructions
        if df is None:
            raise FileNotFoundError(
                f"No software defect dataset found in '{DATASET_DIR}'. "
                "Please place a NASA PROMISE dataset (e.g. kc1.csv, jm1.csv) in the dataset directory, "
                "or run the download script while connected to the internet."
            )

        # Clean column names (lowercase, stripped)
        df.columns = [str(c).strip().lower() for c in df.columns]

        # Identify target column
        target_col = None
        for cand in cls.TARGET_COLUMN_CANDIDATES:
            if cand in df.columns:
                target_col = cand
                break

        if target_col is None:
            # Check the last column
            target_col = df.columns[-1]

        # Extract and standardize target column
        raw_y = df[target_col]
        y = cls._clean_target(raw_y)

        # Extract features (drop target)
        X = df.drop(columns=[target_col]).copy()

        # Rename columns to standard names where possible
        new_cols = {}
        for col in X.columns:
            cleaned = col.replace(" ", "").replace("_", "").lower()
            if cleaned in cls.METRIC_RENAME_MAP:
                new_cols[col] = cls.METRIC_RENAME_MAP[cleaned]
            elif col in cls.METRIC_RENAME_MAP:
                new_cols[col] = cls.METRIC_RENAME_MAP[col]
            else:
                new_cols[col] = col
        X.rename(columns=new_cols, inplace=True)

        # Convert all features to numeric, coerce errors, fill missing with median
        for col in X.columns:
            X[col] = pd.to_numeric(X[col], errors="coerce")
            if X[col].isna().any():
                median_val = X[col].median()
                X[col] = X[col].fillna(median_val if not pd.isna(median_val) else 0)

        # Drop constant columns if any
        constant_cols = [c for c in X.columns if X[c].nunique() <= 1]
        if constant_cols:
            X.drop(columns=constant_cols, inplace=True)

        # Remove duplicate rows
        combined = pd.concat([X, y.rename("target")], axis=1).drop_duplicates()
        y = combined["target"].astype(int)
        X = combined.drop(columns=["target"])

        feature_names = list(X.columns)

        # Metadata
        total_samples = len(X)
        defective_count = int(y.sum())
        clean_count = total_samples - defective_count
        imbalance_ratio = round(clean_count / max(1, defective_count), 2)

        metadata = {
            "source": source_desc,
            "total_samples": total_samples,
            "defective_count": defective_count,
            "clean_count": clean_count,
            "defect_percentage": round((defective_count / total_samples) * 100, 2),
            "imbalance_ratio": imbalance_ratio,
            "feature_count": len(feature_names),
            "feature_names": feature_names,
        }

        return X, y, feature_names, metadata

    @classmethod
    def _clean_target(cls, raw_target: pd.Series) -> pd.Series:
        """Converts diverse defect label formats into binary 0 (clean) and 1 (defective)."""
        def _map_val(val: Any) -> int:
            if pd.isna(val):
                return 0
            if isinstance(val, (bool, np.bool_)):
                return 1 if val else 0
            s = str(val).strip().lower()
            if s in ["true", "y", "yes", "1", "1.0", "defective", "bug"]:
                return 1
            if s in ["false", "n", "no", "0", "0.0", "clean", "none"]:
                return 0
            try:
                num = float(s)
                return 1 if num > 0 else 0
            except ValueError:
                return 0

        return raw_target.apply(_map_val).astype(int)
