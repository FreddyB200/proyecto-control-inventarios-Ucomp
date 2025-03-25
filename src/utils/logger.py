"""Logging utilities."""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class Logger:
    """Application logger."""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize logger.
        
        Args:
            log_dir: Directory for log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("inventario")
        self.logger.setLevel(logging.DEBUG)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # File handler
        log_file = self.log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def debug(self, message: str) -> None:
        """Log debug message.
        
        Args:
            message: Message to log
        """
        self.logger.debug(message)
        
    def info(self, message: str) -> None:
        """Log info message.
        
        Args:
            message: Message to log
        """
        self.logger.info(message)
        
    def warning(self, message: str) -> None:
        """Log warning message.
        
        Args:
            message: Message to log
        """
        self.logger.warning(message)
        
    def error(self, message: str, exc_info: Optional[Exception] = None) -> None:
        """Log error message.
        
        Args:
            message: Message to log
            exc_info: Optional exception to include in log
        """
        self.logger.error(message, exc_info=exc_info)
        
    def critical(self, message: str, exc_info: Optional[Exception] = None) -> None:
        """Log critical message.
        
        Args:
            message: Message to log
            exc_info: Optional exception to include in log
        """
        self.logger.critical(message, exc_info=exc_info)
        
    def set_level(self, level: int) -> None:
        """Set logging level.
        
        Args:
            level: Logging level (e.g., logging.DEBUG)
        """
        self.logger.setLevel(level)
        
    def get_log_file(self) -> Path:
        """Get current log file path.
        
        Returns:
            Path to current log file
        """
        return self.log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
    def clear_old_logs(self, days: int = 30) -> None:
        """Clear log files older than specified days.
        
        Args:
            days: Number of days to keep logs
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for log_file in self.log_dir.glob("app_*.log"):
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink() 