"""
Build cache system for tracking file changes and build state.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Set

from domain.exceptions import CacheException


class BuildCache:
    """
    Manages build cache for tracking file changes and dependencies.
    
    The cache stores:
    - File hashes to detect changes
    - Build timestamps for each task
    - Task results and metadata
    """
    
    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self._dirty = False
    
    def _load_cache(self) -> Dict:
        """Load cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    # Ensure required sections exist
                    data.setdefault("files", {})
                    data.setdefault("builds", {})
                    data.setdefault("tasks", {})
                    return data
            except (json.JSONDecodeError, IOError) as e:
                # Log warning but don't fail - just start fresh
                print(f"Warning: Could not load cache: {e}")
                return self._empty_cache()
        return self._empty_cache()
    
    def _empty_cache(self) -> Dict:
        """Create an empty cache structure."""
        return {
            "files": {},      # file_path -> hash
            "builds": {},     # step -> timestamp
            "tasks": {},      # pdf_id -> task_name -> result
            "version": "2.0"  # Cache format version
        }
    
    def save(self):
        """Save cache to disk if it has been modified."""
        if not self._dirty:
            return
            
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Write to temp file first for atomicity
            temp_file = self.cache_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
            
            # Atomic rename
            temp_file.replace(self.cache_file)
            self._dirty = False
        except IOError as e:
            raise CacheException(f"Failed to save cache: {e}")
    
    def get_file_hash(self, path: Path) -> str:
        """Calculate MD5 hash of a file."""
        if not path.exists():
            return ""
        
        hasher = hashlib.md5()
        try:
            with open(path, 'rb') as f:
                # Read in chunks for large files
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except IOError:
            return ""
    
    def has_file_changed(self, path: Path) -> bool:
        """Check if a file has changed since last build."""
        path_str = str(path.absolute())
        current_hash = self.get_file_hash(path)
        
        if not current_hash:  # File doesn't exist
            return path_str in self.cache["files"]
        
        if path_str not in self.cache["files"]:
            return True
        
        return self.cache["files"][path_str] != current_hash
    
    def update_file(self, path: Path):
        """Update file hash in cache."""
        path_str = str(path.absolute())
        new_hash = self.get_file_hash(path)
        
        if new_hash:  # Only cache existing files
            if self.cache["files"].get(path_str) != new_hash:
                self.cache["files"][path_str] = new_hash
                self._dirty = True
    
    def remove_file(self, path: Path):
        """Remove a file from the cache."""
        path_str = str(path.absolute())
        if path_str in self.cache["files"]:
            del self.cache["files"][path_str]
            self._dirty = True
    
    def update_files(self, paths: List[Path]):
        """Update multiple files at once."""
        for path in paths:
            self.update_file(path)
    
    def mark_build_complete(self, step: str):
        """Mark a build step as complete with current timestamp."""
        self.cache["builds"][step] = datetime.now().isoformat()
        self._dirty = True
    
    def get_last_build_time(self, step: str) -> Optional[datetime]:
        """Get the last build time for a step."""
        if step in self.cache["builds"]:
            try:
                return datetime.fromisoformat(self.cache["builds"][step])
            except ValueError:
                return None
        return None
    
    def record_task_result(self, pdf_id: str, task_name: str, result: Dict):
        """Record the result of a task for a specific PDF."""
        if pdf_id not in self.cache["tasks"]:
            self.cache["tasks"][pdf_id] = {}
        
        self.cache["tasks"][pdf_id][task_name] = {
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        self._dirty = True
    
    def get_task_result(self, pdf_id: str, task_name: str) -> Optional[Dict]:
        """Get the cached result of a task."""
        return self.cache["tasks"].get(pdf_id, {}).get(task_name)
    
    def get_changed_files(self, pattern: str = "*.md") -> Set[Path]:
        """Get all files matching pattern that have changed."""
        changed = set()
        
        for file_path in self.cache["files"]:
            path = Path(file_path)
            if path.match(pattern) and self.has_file_changed(path):
                changed.add(path)
        
        return changed
    
    def clean_missing_files(self):
        """Remove entries for files that no longer exist."""
        to_remove = []
        
        for file_path in self.cache["files"]:
            if not Path(file_path).exists():
                to_remove.append(file_path)
        
        for path in to_remove:
            del self.cache["files"][path]
            self._dirty = True
        
        return len(to_remove)
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "total_files": len(self.cache["files"]),
            "total_builds": len(self.cache["builds"]),
            "total_task_results": sum(
                len(tasks) for tasks in self.cache["tasks"].values()
            ),
            "cache_file": str(self.cache_file),
            "version": self.cache.get("version", "1.0")
        }
    
    def clear(self):
        """Clear all cache data."""
        self.cache = self._empty_cache()
        self._dirty = True
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Auto-save on context exit."""
        self.save()
        return False