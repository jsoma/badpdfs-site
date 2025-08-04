"""
Domain models for the PDF Gallery processor.

These models represent the core business objects in our system:
- PDFExample: A PDF with one or more extraction approaches
- Approach: A single markdown file showing how to extract from a PDF
- Gallery: The collection of all PDF examples
"""

import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class CodeBlock:
    """Represents a code block in a markdown file."""
    content: str
    language: str = "python"
    line_number: int = 0
    
    def __str__(self):
        return f"CodeBlock({self.language}, {len(self.content)} chars)"


@dataclass
class Approach:
    """Represents a single markdown file showing a PDF extraction approach."""
    file: Path
    pdf_example: Optional['PDFExample'] = None
    _metadata: Optional[Dict[str, Any]] = field(default=None, init=False)
    _content: Optional[str] = field(default=None, init=False)
    _code_blocks: Optional[List[CodeBlock]] = field(default=None, init=False)
    
    @property
    def slug(self) -> str:
        """Get the slug for this approach (filename without extension)."""
        return self.file.stem
    
    @property
    def content(self) -> str:
        """Lazy load file content."""
        if self._content is None:
            self._content = self.file.read_text(encoding='utf-8')
        return self._content
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Extract and cache YAML frontmatter."""
        if self._metadata is None:
            self._metadata = self._extract_metadata()
        return self._metadata
    
    @property
    def code_blocks(self) -> List[CodeBlock]:
        """Extract and cache code blocks."""
        if self._code_blocks is None:
            self._code_blocks = self._extract_code_blocks()
        return self._code_blocks
    
    def _extract_metadata(self) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown content."""
        content = self.content
        if not content.startswith('---'):
            return {}
        
        try:
            # Find the closing ---
            end_index = content.index('---', 3)
            yaml_content = content[3:end_index].strip()
            metadata = yaml.safe_load(yaml_content) or {}
            
            # Add computed fields
            metadata['slug'] = self.slug
            metadata['file'] = self.file.name
            
            return metadata
        except (ValueError, yaml.YAMLError):
            return {}
    
    def _extract_code_blocks(self) -> List[CodeBlock]:
        """Extract code blocks from markdown content."""
        import re
        blocks = []
        
        # Match ```language\ncode\n```
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(pattern, self.content, re.DOTALL)
        
        for lang, code in matches:
            language = lang or 'python'
            blocks.append(CodeBlock(
                content=code,
                language=language
            ))
        
        return blocks
    
    def is_published(self) -> bool:
        """Check if this approach is published."""
        return self.metadata.get('published', False)
    
    def get_title(self) -> str:
        """Get the title of this approach."""
        return self.metadata.get('title', 'Untitled')
    
    def get_methods(self) -> List[str]:
        """Get the natural-pdf methods used in this approach."""
        return self.metadata.get('methods', [])


@dataclass
class PDFExample:
    """Represents a PDF with all its extraction approaches."""
    id: str
    base_dir: Path
    _metadata: Optional[Dict[str, Any]] = field(default=None, init=False)
    _approaches: Optional[List[Approach]] = field(default=None, init=False)
    _pdf_files: Optional[List[Path]] = field(default=None, init=False)
    
    @property
    def approaches(self) -> List[Approach]:
        """Lazy load approaches (markdown files)."""
        if self._approaches is None:
            self._approaches = self._load_approaches()
        return self._approaches
    
    @property
    def pdf_files(self) -> List[Path]:
        """Lazy load PDF files."""
        if self._pdf_files is None:
            self._pdf_files = list(self.base_dir.glob("*.pdf"))
        return self._pdf_files
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Combined metadata from all approaches."""
        if self._metadata is None:
            self._metadata = self._compute_metadata()
        return self._metadata
    
    def _load_approaches(self) -> List[Approach]:
        """Load all markdown files as approaches."""
        approaches = []
        for md_file in sorted(self.base_dir.glob("*.md")):
            approach = Approach(file=md_file, pdf_example=self)
            approaches.append(approach)
        return approaches
    
    def _compute_metadata(self) -> Dict[str, Any]:
        """Compute combined metadata from all approaches."""
        # Start with metadata from first published approach
        published_approaches = [a for a in self.approaches if a.is_published()]
        if not published_approaches:
            return {"id": self.id, "published": False}
        
        # Use first published approach as base
        metadata = published_approaches[0].metadata.copy()
        metadata["id"] = self.id
        metadata["approaches"] = [a.file.name for a in self.approaches]
        
        # Collect all methods from all approaches
        all_methods = set()
        for approach in published_approaches:
            all_methods.update(approach.get_methods())
        metadata["methods"] = sorted(all_methods)
        
        # Get PDF info
        if self.pdf_files:
            pdf_file = self.pdf_files[0]
            metadata["pdf"] = pdf_file.name
            metadata["pdf_size"] = pdf_file.stat().st_size / (1024 * 1024)  # MB
        
        return metadata
    
    def is_published(self) -> bool:
        """Check if any approach is published."""
        return any(approach.is_published() for approach in self.approaches)
    
    def get_primary_pdf(self) -> Optional[Path]:
        """Get the primary PDF file."""
        if self.pdf_files:
            # Try to match the PDF mentioned in metadata
            pdf_name = self.metadata.get("pdf")
            if pdf_name:
                for pdf in self.pdf_files:
                    if pdf.name == pdf_name:
                        return pdf
            # Fall back to first PDF
            return self.pdf_files[0]
        return None
    
    def get_artifacts_dir(self, artifacts_root: Path) -> Path:
        """Get the artifacts directory for this PDF."""
        return artifacts_root / "pdfs" / self.id
    
    def __repr__(self):
        return f"PDFExample(id='{self.id}', approaches={len(self.approaches)}, published={self.is_published()})"


class Gallery:
    """Collection of all PDF examples."""
    
    def __init__(self, content_dir: Path, artifacts_dir: Path):
        self.content_dir = content_dir
        self.artifacts_dir = artifacts_dir
        self._examples: Optional[Dict[str, PDFExample]] = None
    
    @property
    def examples(self) -> Dict[str, PDFExample]:
        """Lazy load all PDF examples."""
        if self._examples is None:
            self._examples = self._load_all()
        return self._examples
    
    def _load_all(self) -> Dict[str, PDFExample]:
        """Load all PDF examples from the content directory."""
        examples = {}
        pdfs_dir = self.content_dir / "pdfs"
        
        if not pdfs_dir.exists():
            return examples
        
        for pdf_dir in pdfs_dir.iterdir():
            if pdf_dir.is_dir():
                example = PDFExample(
                    id=pdf_dir.name,
                    base_dir=pdf_dir
                )
                examples[example.id] = example
        
        return examples
    
    def get_published(self) -> List[PDFExample]:
        """Get all published PDF examples."""
        return [ex for ex in self.examples.values() if ex.is_published()]
    
    def get_by_method(self, method: str) -> List[PDFExample]:
        """Get all examples that use a specific method."""
        results = []
        for example in self.get_published():
            if method in example.metadata.get("methods", []):
                results.append(example)
        return results
    
    def get_example(self, pdf_id: str) -> Optional[PDFExample]:
        """Get a specific example by ID."""
        return self.examples.get(pdf_id)
    
    def get_all_methods(self) -> List[str]:
        """Get all unique methods used across all examples."""
        methods = set()
        for example in self.get_published():
            methods.update(example.metadata.get("methods", []))
        return sorted(methods)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the gallery."""
        published = self.get_published()
        total_approaches = sum(len(ex.approaches) for ex in published)
        
        return {
            "total_pdfs": len(self.examples),
            "published_pdfs": len(published),
            "total_approaches": total_approaches,
            "unique_methods": len(self.get_all_methods()),
            "methods": self.get_all_methods()
        }
    
    def __repr__(self):
        return f"Gallery(examples={len(self.examples)}, published={len(self.get_published())})"