"""
SQLite Database and Analysis History module.
Stores metadata, risk distributions, and summaries of past code analyses
without permanently storing sensitive user source code.
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from config.settings import DATABASE_PATH


class HistoryDatabase:
    """Manages SQLite storage of code analysis history."""

    @classmethod
    def _get_connection(cls) -> sqlite3.Connection:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls) -> None:
        """Initializes the database schema if not present."""
        with cls._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    function_count INTEGER NOT NULL,
                    low_risk_count INTEGER NOT NULL,
                    medium_risk_count INTEGER NOT NULL,
                    high_risk_count INTEGER NOT NULL,
                    avg_cyclomatic_complexity REAL NOT NULL,
                    total_loc INTEGER NOT NULL,
                    static_issues_count INTEGER NOT NULL,
                    summary TEXT NOT NULL
                )
                """
            )
            conn.commit()

    @classmethod
    def save_analysis(
        cls,
        filename: str,
        function_count: int,
        low_risk_count: int,
        medium_risk_count: int,
        high_risk_count: int,
        avg_cyclomatic_complexity: float,
        total_loc: int,
        static_issues_count: int,
        summary: str,
    ) -> int:
        """Saves a new analysis session record and returns its ID."""
        cls.init_db()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO analysis_history (
                    filename, timestamp, function_count,
                    low_risk_count, medium_risk_count, high_risk_count,
                    avg_cyclomatic_complexity, total_loc, static_issues_count, summary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    filename,
                    timestamp,
                    function_count,
                    low_risk_count,
                    medium_risk_count,
                    high_risk_count,
                    avg_cyclomatic_complexity,
                    total_loc,
                    static_issues_count,
                    summary,
                ),
            )
            conn.commit()
            return cursor.lastrowid or 0

    @classmethod
    def get_all_analyses(cls, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves past analyses sorted by recency."""
        cls.init_db()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM analysis_history ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @classmethod
    def clear_history(cls) -> None:
        """Deletes all records from analysis history table."""
        cls.init_db()
        with cls._get_connection() as conn:
            conn.execute("DELETE FROM analysis_history")
            conn.commit()

    @classmethod
    def get_summary_stats(cls) -> Dict[str, Any]:
        """Calculates aggregate statistics over past analyses."""
        cls.init_db()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    COUNT(*) as total_files,
                    COALESCE(SUM(function_count), 0) as total_functions,
                    COALESCE(SUM(low_risk_count), 0) as total_low_risk,
                    COALESCE(SUM(medium_risk_count), 0) as total_medium_risk,
                    COALESCE(SUM(high_risk_count), 0) as total_high_risk,
                    COALESCE(AVG(avg_cyclomatic_complexity), 0.0) as overall_avg_cc,
                    COALESCE(SUM(total_loc), 0) as total_loc_analyzed
                FROM analysis_history
                """
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {
                "total_files": 0,
                "total_functions": 0,
                "total_low_risk": 0,
                "total_medium_risk": 0,
                "total_high_risk": 0,
                "overall_avg_cc": 0.0,
                "total_loc_analyzed": 0,
            }
