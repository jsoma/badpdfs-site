"""
Search index generation task for PDF Gallery.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

from domain import PDFExample
from tasks import BatchTask, TaskContext


class SearchIndexTask(BatchTask):
    """
    Task to build search index for the gallery.
    
    This is a batch task that processes all PDFs at once to create:
    - Full-text search index
    - Method reverse index
    - Search suggestions
    """
    
    def __init__(self):
        super().__init__(name="search_index", dependencies=["metadata", "execution"])
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were'
        }
    
    def process_batch(self, pdfs: List[PDFExample], context: TaskContext) -> Dict[str, Any]:
        """Build search index from all PDFs."""
        documents = []
        all_metadata = []
        
        # Collect data from all PDFs
        for pdf in pdfs:
            # Skip unpublished
            if not pdf.is_published():
                continue
            
            # Load metadata
            metadata_path = context.get_artifact_path(pdf, "metadata.json")
            if metadata_path.exists():
                metadata_list = context.read_artifact(metadata_path)
                
                for metadata in metadata_list:
                    # Load execution results if available
                    slug = metadata.get("slug")
                    execution_path = context.get_artifact_path(
                        pdf, "executions", f"{slug}.json"
                    )
                    
                    execution = {}
                    if execution_path.exists():
                        execution = context.read_artifact(execution_path)
                    
                    # Build search document
                    doc = self._build_document(metadata, execution, context)
                    documents.append(doc)
                    all_metadata.append(metadata)
        
        # Build indices
        method_index = self._build_method_index(all_metadata)
        suggestions = self._build_suggestions(all_metadata)
        
        # Create full index
        full_index = {
            "documents": documents,
            "methodIndex": method_index,
            "suggestions": suggestions,
            "stats": {
                "totalDocuments": len(documents),
                "totalMethods": len(method_index),
                "indexVersion": "2.0"
            }
        }
        
        # Save full index
        full_path = context.artifacts_dir / "search_index.json"
        context.write_artifact(full_path, full_index)
        
        # Create compact version
        compact_index = self._create_compact_index(full_index)
        compact_path = context.artifacts_dir / "search_index.compact.json"
        
        # Save compact version without pretty printing
        compact_path.parent.mkdir(parents=True, exist_ok=True)
        with open(compact_path, 'w') as f:
            json.dump(compact_index, f, separators=(',', ':'))
        
        return {
            "documents_indexed": len(documents),
            "methods_indexed": len(method_index),
            "index_size": full_path.stat().st_size if full_path.exists() else 0,
            "compact_size": compact_path.stat().st_size if compact_path.exists() else 0
        }
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Inputs are metadata and execution results."""
        # Note: This is called per-PDF but we're a batch task
        # Return empty list since we handle inputs in process_batch
        return []
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files - not used for batch tasks."""
        # BatchTask doesn't use per-PDF outputs
        return []
    
    def get_batch_outputs(self, context: TaskContext) -> List[Path]:
        """Output files for the batch task."""
        return [
            context.artifacts_dir / "search_index.json",
            context.artifacts_dir / "search_index.compact.json"
        ]
    
    def _build_document(self, metadata: Dict[str, Any], 
                       execution: Dict[str, Any],
                       context: TaskContext) -> Dict[str, Any]:
        """Build a search document from metadata and execution."""
        # Extract searchable content
        content = self._extract_content(execution)
        code = self._extract_code(execution)
        
        return {
            "id": metadata.get("id", ""),
            "slug": metadata.get("slug", ""),
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "content": content,
            "code": code,
            "methods": metadata.get("methods", []),
            "selectors": metadata.get("selectors", []),
            "tags": metadata.get("tags", []),
            "complexity": metadata.get("complexity", {}).get("code_blocks", 0),
            "pdf": metadata.get("pdf", "")
        }
    
    def _extract_content(self, execution: Dict[str, Any]) -> str:
        """Extract searchable text content."""
        if not execution or "cells" not in execution:
            return ""
        
        content_parts = []
        
        for cell in execution.get("cells", []):
            if cell["type"] == "markdown":
                # Clean markdown
                text = cell["content"]
                text = re.sub(r'#+ ', '', text)  # Remove headers
                text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold
                text = re.sub(r'\*(.*?)\*', r'\1', text)  # Remove italic
                text = re.sub(r'`(.*?)`', r'\1', text)  # Remove inline code
                content_parts.append(text)
            elif cell["type"] == "code":
                # Include code content
                content_parts.append(cell["content"])
            elif cell["type"] == "tab":
                # Process tab cells
                for tab_cell in cell.get("cells", []):
                    if tab_cell["type"] == "markdown":
                        content_parts.append(tab_cell["content"])
                    elif tab_cell["type"] == "code":
                        content_parts.append(tab_cell["content"])
        
        return "\n".join(content_parts)
    
    def _extract_code(self, execution: Dict[str, Any]) -> str:
        """Extract only code content."""
        if not execution or "cells" not in execution:
            return ""
        
        code_parts = []
        
        for cell in execution.get("cells", []):
            if cell["type"] == "code":
                code_parts.append(cell["content"])
            elif cell["type"] == "tab":
                for tab_cell in cell.get("cells", []):
                    if tab_cell["type"] == "code":
                        code_parts.append(tab_cell["content"])
        
        return "\n".join(code_parts)
    
    def _build_method_index(self, metadata_list: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Build reverse index of methods to document IDs."""
        method_index = defaultdict(set)
        
        for item in metadata_list:
            doc_id = item.get("id", "")
            for method in item.get("methods", []):
                method_index[method].add(doc_id)
        
        # Convert to regular dict with sorted lists
        return {
            method: sorted(list(doc_ids)) 
            for method, doc_ids in sorted(method_index.items())
        }
    
    def _build_suggestions(self, metadata_list: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Build search suggestions."""
        methods = set()
        terms = set()
        
        for item in metadata_list:
            # Collect methods
            methods.update(item.get("methods", []))
            
            # Extract terms from titles and descriptions
            text = f"{item.get('title', '')} {item.get('description', '')}"
            words = re.findall(r'\b\w+\b', text.lower())
            
            # Filter stop words and short words
            for word in words:
                if len(word) > 3 and word not in self.stop_words:
                    terms.add(word)
        
        return {
            "methods": sorted(list(methods)),
            "terms": sorted(list(terms))[:50]  # Top 50 terms
        }
    
    def _create_compact_index(self, full_index: Dict[str, Any]) -> Dict[str, Any]:
        """Create a compact version of the index."""
        compact_docs = []
        
        for doc in full_index["documents"]:
            # Truncate long fields
            compact_doc = doc.copy()
            if len(compact_doc["content"]) > 500:
                compact_doc["content"] = compact_doc["content"][:500] + "..."
            if len(compact_doc["code"]) > 300:
                compact_doc["code"] = compact_doc["code"][:300] + "..."
            
            compact_docs.append(compact_doc)
        
        return {
            "documents": compact_docs,
            "methodIndex": full_index["methodIndex"],
            "suggestions": full_index["suggestions"],
            "stats": full_index["stats"]
        }