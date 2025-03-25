"""Database utilities for SQLite operations."""
import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path

class Database:
    """Database connection and query manager."""
    
    def __init__(self, db_path: str = "src/inventario.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_exists()
        
    def _ensure_db_exists(self) -> None:
        """Ensure database file exists and create if it doesn't."""
        db_file = Path(self.db_path)
        if not db_file.exists():
            db_file.parent.mkdir(parents=True, exist_ok=True)
            
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection.
        
        Returns:
            SQLite connection object
        """
        return sqlite3.connect(self.db_path)
        
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of dictionaries containing query results
        """
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an UPDATE/INSERT/DELETE query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of rows affected
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
            
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute multiple queries in a transaction.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            Number of rows affected
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
            
    def get_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute a SELECT query and return a single result.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Dictionary containing the result or None if not found
        """
        results = self.execute_query(query, params)
        return results[0] if results else None 