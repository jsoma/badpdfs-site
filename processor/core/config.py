"""
Configuration management for the PDF Gallery processor.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """
    Manages configuration from multiple sources:
    1. config.json in project root
    2. Environment variables
    3. Default values
    """
    
    # Default configuration values
    DEFAULTS = {
        "r2_public_url": "https://pub-4e99d31d19cb404d8d4f5f7efa51ef6e.r2.dev",
        "screenshot_dpi": 150,
        "screenshot_max_pages": 10,
        "thumbnail_size": (400, 400),
        "max_execution_time": 30,  # seconds
        "enable_notebooks": True,
        "verbose": False
    }
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self._config = self._load_config()
    
    def _find_project_root(self) -> Path:
        """Find project root by looking for config.json."""
        current = Path.cwd()
        
        # Look up the directory tree
        for parent in [current] + list(current.parents):
            if (parent / "config.json").exists():
                return parent
            # Also check if we're in the processor directory
            if parent.name == "processor" and (parent.parent / "config.json").exists():
                return parent.parent
        
        # Default to current directory
        return current
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from all sources."""
        config = self.DEFAULTS.copy()
        
        # Load from config.json if it exists
        config_file = self.project_root / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config.json: {e}")
        
        # Override with environment variables
        env_mappings = {
            "R2_PUBLIC_URL": "r2_public_url",
            "PDF_GALLERY_VERBOSE": "verbose",
            "PDF_GALLERY_DPI": "screenshot_dpi",
        }
        
        for env_key, config_key in env_mappings.items():
            if env_key in os.environ:
                value = os.environ[env_key]
                # Convert boolean strings
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                # Convert numeric strings
                elif value.isdigit():
                    value = int(value)
                
                config[config_key] = value
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access."""
        return self._config[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists."""
        return key in self._config
    
    @property
    def r2_public_url(self) -> str:
        """Get R2 public URL."""
        return self._config["r2_public_url"]
    
    @property
    def r2_pdf_base_url(self) -> str:
        """Get R2 base URL for PDFs."""
        return f"{self.r2_public_url}/pdfs"
    
    @property
    def screenshot_dpi(self) -> int:
        """Get screenshot DPI."""
        return self._config["screenshot_dpi"]
    
    @property
    def verbose(self) -> bool:
        """Get verbose mode setting."""
        return self._config["verbose"]
    
    @property
    def content_dir(self) -> Path:
        """Get content directory path."""
        return self.project_root / "content"

    @property
    def frontend_dir(self) -> Path:
        """Get content directory path."""
        return self.project_root / "frontend"

    @property
    def artifacts_dir(self) -> Path:
        """Get artifacts directory path."""
        return self.project_root / "artifacts"
    
    @property
    def processor_dir(self) -> Path:
        """Get processor directory path."""
        return self.project_root / "processor"
    
    @property
    def frontend_artifacts_dir(self) -> Path:
        """Get frontend artifacts directory path."""
        return self.project_root / "frontend" / "public" / "artifacts"
    
    def to_dict(self) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return self._config.copy()
    
    def save_to_file(self, path: Optional[Path] = None):
        """Save current configuration to a file."""
        path = path or (self.project_root / "config.json")
        with open(path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def __repr__(self):
        return f"Config(project_root='{self.project_root}', keys={list(self._config.keys())})"