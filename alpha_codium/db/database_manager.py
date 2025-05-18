"""
Database Manager for AlphaCodium

This module provides functionality to store and retrieve problems, solutions,
and model information using SQLite.
"""

import os
import json
import sqlite3
from typing import List, Dict, Any, Optional

from alpha_codium.log import get_logger

class DatabaseManager:
    """
    A class to manage the SQLite database for AlphaCodium.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the DatabaseManager.
        
        Args:
            db_path: Path to the SQLite database file. If None, uses ~/.alpha_codium/alpha_codium.db
        """
        self.logger = get_logger(__name__)
        
        # Set up database path
        if db_path is None:
            home_dir = os.path.expanduser("~")
            db_dir = os.path.join(home_dir, ".alpha_codium")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "alpha_codium.db")
        
        self.db_path = db_path
        self.logger.info(f"Using database at {self.db_path}")
        
        # Initialize the database
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema if it doesn't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create problems table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                test_cases TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create solutions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER,
                model_id TEXT NOT NULL,
                code TEXT NOT NULL,
                execution_time REAL,
                success BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            )
            ''')
            
            # Create models table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                description TEXT,
                input_token_limit INTEGER,
                output_token_limit INTEGER,
                last_used TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create execution_logs table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solution_id INTEGER,
                test_case TEXT NOT NULL,
                expected_output TEXT NOT NULL,
                actual_output TEXT NOT NULL,
                passed BOOLEAN,
                execution_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (solution_id) REFERENCES solutions (id)
            )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
    
    def save_problem(self, problem: Dict[str, Any]) -> int:
        """
        Save a problem to the database.
        
        Args:
            problem: The problem data
            
        Returns:
            The ID of the saved problem
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if problem already exists
            cursor.execute(
                "SELECT id FROM problems WHERE name = ? AND description = ?",
                (problem.get("name", ""), problem.get("description", ""))
            )
            existing = cursor.fetchone()
            
            if existing:
                problem_id = existing[0]
                # Update the problem
                cursor.execute(
                    "UPDATE problems SET test_cases = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (json.dumps(problem.get("public_tests", [])), problem_id)
                )
            else:
                # Insert new problem
                cursor.execute(
                    "INSERT INTO problems (name, description, test_cases) VALUES (?, ?, ?)",
                    (
                        problem.get("name", ""),
                        problem.get("description", ""),
                        json.dumps(problem.get("public_tests", []))
                    )
                )
                problem_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return problem_id
            
        except Exception as e:
            self.logger.error(f"Error saving problem: {e}")
            return -1
    
    def get_problem(self, problem_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a problem from the database.
        
        Args:
            problem_id: The ID of the problem
            
        Returns:
            The problem data, or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM problems WHERE id = ?",
                (problem_id,)
            )
            row = cursor.fetchone()
            
            if row:
                problem = dict(row)
                problem["public_tests"] = json.loads(problem["test_cases"])
                del problem["test_cases"]
                return problem
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting problem: {e}")
            return None
        finally:
            conn.close()
    
    def save_solution(self, problem_id: int, model_id: str, code: str, 
                     execution_time: float, success: bool) -> int:
        """
        Save a solution to the database.
        
        Args:
            problem_id: The ID of the problem
            model_id: The ID of the model used
            code: The solution code
            execution_time: The execution time in seconds
            success: Whether the solution was successful
            
        Returns:
            The ID of the saved solution
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO solutions (problem_id, model_id, code, execution_time, success) VALUES (?, ?, ?, ?, ?)",
                (problem_id, model_id, code, execution_time, success)
            )
            
            solution_id = cursor.lastrowid
            
            # Update model usage
            cursor.execute(
                "INSERT OR IGNORE INTO models (id, display_name, usage_count) VALUES (?, ?, 0)",
                (model_id, model_id)
            )
            
            cursor.execute(
                "UPDATE models SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP WHERE id = ?",
                (model_id,)
            )
            
            conn.commit()
            conn.close()
            
            return solution_id
            
        except Exception as e:
            self.logger.error(f"Error saving solution: {e}")
            return -1
    
    def get_solution(self, solution_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a solution from the database.
        
        Args:
            solution_id: The ID of the solution
            
        Returns:
            The solution data, or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM solutions WHERE id = ?",
                (solution_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting solution: {e}")
            return None
        finally:
            conn.close()
    
    def get_solutions_for_problem(self, problem_id: int) -> List[Dict[str, Any]]:
        """
        Get all solutions for a problem.
        
        Args:
            problem_id: The ID of the problem
            
        Returns:
            A list of solution data dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM solutions WHERE problem_id = ? ORDER BY created_at DESC",
                (problem_id,)
            )
            rows = cursor.fetchall()
            
            solutions = [dict(row) for row in rows]
            conn.close()
            
            return solutions
            
        except Exception as e:
            self.logger.error(f"Error getting solutions for problem: {e}")
            return []
    
    def save_model_info(self, model_info: Dict[str, Any]) -> bool:
        """
        Save model information to the database.
        
        Args:
            model_info: The model information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT OR REPLACE INTO models 
                (id, display_name, description, input_token_limit, output_token_limit, updated_at) 
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    model_info.get("id", ""),
                    model_info.get("display_name", ""),
                    model_info.get("description", ""),
                    model_info.get("input_token_limit", 0),
                    model_info.get("output_token_limit", 0)
                )
            )
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving model info: {e}")
            return False
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get model information from the database.
        
        Args:
            model_id: The ID of the model
            
        Returns:
            The model information, or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM models WHERE id = ?",
                (model_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting model info: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_models(self) -> List[Dict[str, Any]]:
        """
        Get all model information from the database.
        
        Returns:
            A list of model information dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM models ORDER BY usage_count DESC, last_used DESC"
            )
            rows = cursor.fetchall()
            
            models = [dict(row) for row in rows]
            conn.close()
            
            return models
            
        except Exception as e:
            self.logger.error(f"Error getting all models: {e}")
            return []
    
    def get_recent_problems(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recently updated problems.
        
        Args:
            limit: The maximum number of problems to return
            
        Returns:
            A list of problem dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM problems ORDER BY updated_at DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            
            problems = []
            for row in rows:
                problem = dict(row)
                problem["public_tests"] = json.loads(problem["test_cases"])
                del problem["test_cases"]
                problems.append(problem)
            
            conn.close()
            
            return problems
            
        except Exception as e:
            self.logger.error(f"Error getting recent problems: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the database.
        
        Returns:
            A dictionary of statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get problem count
            cursor.execute("SELECT COUNT(*) FROM problems")
            problem_count = cursor.fetchone()[0]
            
            # Get solution count
            cursor.execute("SELECT COUNT(*) FROM solutions")
            solution_count = cursor.fetchone()[0]
            
            # Get model count
            cursor.execute("SELECT COUNT(*) FROM models")
            model_count = cursor.fetchone()[0]
            
            # Get success rate
            cursor.execute("SELECT COUNT(*) FROM solutions WHERE success = 1")
            success_count = cursor.fetchone()[0]
            success_rate = 0
            if solution_count > 0:
                success_rate = (success_count / solution_count) * 100
            
            # Get average execution time
            cursor.execute("SELECT AVG(execution_time) FROM solutions")
            avg_execution_time = cursor.fetchone()[0] or 0
            
            # Get most used model
            cursor.execute(
                "SELECT id, display_name, usage_count FROM models ORDER BY usage_count DESC LIMIT 1"
            )
            most_used_model = cursor.fetchone()
            
            conn.close()
            
            return {
                "problem_count": problem_count,
                "solution_count": solution_count,
                "model_count": model_count,
                "success_rate": success_rate,
                "avg_execution_time": avg_execution_time,
                "most_used_model": most_used_model[1] if most_used_model else None,
                "most_used_model_count": most_used_model[2] if most_used_model else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {
                "problem_count": 0,
                "solution_count": 0,
                "model_count": 0,
                "success_rate": 0,
                "avg_execution_time": 0,
                "most_used_model": None,
                "most_used_model_count": 0
            }