"""Configuration utilities."""
import json
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """Configuration manager."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Dictionary containing configuration
        """
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_config()
        
    def _save_config(self) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
            
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Dictionary containing default configuration
        """
        return {
            "database": {
                "path": "src/inventario.db",
                "backup_dir": "backups"
            },
            "ui": {
                "theme": "light",
                "language": "es",
                "window_size": {
                    "width": 1024,
                    "height": 768
                }
            },
            "reports": {
                "export_dir": "reports",
                "default_format": "excel"
            },
            "security": {
                "password_min_length": 8,
                "session_timeout": 30
            }
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key (can use dots for nested keys)
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
                
        return value if value is not None else default
        
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key (can use dots for nested keys)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            config = config.setdefault(k, {})
            
        config[keys[-1]] = value
        self._save_config()
        
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values.
        
        Args:
            updates: Dictionary of updates
        """
        def update_dict(d: Dict[str, Any], u: Dict[str, Any]) -> None:
            for k, v in u.items():
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    update_dict(d[k], v)
                else:
                    d[k] = v
                    
        update_dict(self.config, updates)
        self._save_config()
        
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self._get_default_config()
        self._save_config() 