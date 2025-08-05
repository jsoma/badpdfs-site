"""
Jupyter notebook generation task for PDF Gallery.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

from domain import PDFExample, Approach
from tasks import Task, TaskContext


class NotebookTask(Task):
    """
    Task to generate Jupyter notebooks from markdown files.
    
    This includes:
    - Converting markdown to notebook format
    - Adding installation cells
    - Adding PDF download cells
    - Preserving code structure
    """
    
    def __init__(self):
        super().__init__(name="notebooks", dependencies=["metadata"])
    
    def process(self, pdf: PDFExample, context: TaskContext) -> Dict[str, Any]:
        """Generate notebooks for all published approaches."""
        results = []
        pdf_base_url = context.config.get("r2_public_url", "")
        
        for approach in pdf.approaches:
            if not approach.is_published():
                continue
            
            context.log(f"Generating notebook for {approach.slug}")
            
            # Create notebook
            notebook = self._create_notebook(approach, pdf, pdf_base_url)
            
            if notebook:
                # Save notebook
                notebook_path = context.get_artifact_path(
                    pdf, "notebooks", f"{approach.slug}.ipynb"
                )
                context.write_artifact(notebook_path, notebook)
                
                results.append({
                    'approach': approach.slug,
                    'status': 'success',
                    'path': str(notebook_path.relative_to(context.artifacts_dir))
                })
            else:
                results.append({
                    'approach': approach.slug,
                    'status': 'skipped',
                    'reason': 'No PDF file specified'
                })
        
        # Create manifest for this PDF
        if results:
            manifest = {
                'pdf_id': pdf.id,
                'notebooks': results,
                'pdf_base_url': pdf_base_url
            }
            manifest_path = context.get_artifact_path(pdf, "notebooks", "manifest.json")
            context.write_artifact(manifest_path, manifest)
        
        return {"notebooks_created": len(results), "results": results}
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Input files are markdown files."""
        return [approach.file for approach in pdf.approaches if approach.is_published()]
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files are notebooks."""
        outputs = []
        for approach in pdf.approaches:
            if approach.is_published():
                outputs.append(
                    context.get_artifact_path(pdf, "notebooks", f"{approach.slug}.ipynb")
                )
        # Also include manifest
        if any(a.is_published() for a in pdf.approaches):
            outputs.append(context.get_artifact_path(pdf, "notebooks", "manifest.json"))
        
        return outputs
    
    def _create_notebook(self, approach: Approach, pdf: PDFExample,
                        pdf_base_url: str) -> Optional[Dict[str, Any]]:
        """Create a Jupyter notebook from an approach."""
        metadata = approach.metadata
        
        # Skip if no PDF specified
        pdf_filename = metadata.get('pdf', '')
        if not pdf_filename:
            return None
        
        # Create notebook structure
        notebook = {
            "cells": [],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        # Add title and description
        title = metadata.get('title', 'Untitled')
        description = metadata.get('description', '')
        
        notebook["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {title}\n",
                "\n",
                f"{description}\n"
            ]
        })
        
        # Add installation cell
        notebook["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Install natural-pdf\n",
                "!pip install natural-pdf"
            ]
        })
        
        # Add PDF download cell
        pdf_url = f"{pdf_base_url}/pdfs/{pdf.id}/{pdf_filename}"
        notebook["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Download the PDF file\n",
                "import urllib.request\n",
                "import os\n",
                "\n",
                f'pdf_url = "{pdf_url}"\n',
                f'pdf_name = "{pdf_filename}"\n',
                "\n",
                "if not os.path.exists(pdf_name):\n",
                "    print(f\"Downloading {pdf_name}...\")\n",
                "    urllib.request.urlretrieve(pdf_url, pdf_name)\n",
                "    print(f\"Downloaded {pdf_name}\")\n",
                "else:\n",
                "    print(f\"{pdf_name} already exists\")"
            ]
        })
        
        # Parse the full content to preserve markdown and code order
        content = approach.content
        
        # Remove frontmatter
        if content.startswith('---'):
            try:
                end_index = content.index('---', 3)
                content = content[end_index + 3:].strip()
            except ValueError:
                pass
        
        # Split content into sections (markdown and code blocks)
        import re
        
        # Pattern to match code blocks (including language)
        code_pattern = r'```(\w*)\n(.*?)\n```'
        
        # Split the content by code blocks
        parts = re.split(code_pattern, content, flags=re.DOTALL)
        
        # Process parts: parts[0] is markdown, then alternates: lang, code, markdown, lang, code, etc.
        i = 0
        while i < len(parts):
            if i % 3 == 0:  # Markdown sections
                markdown_content = parts[i].strip()
                if markdown_content:
                    # Split into lines and add newlines
                    lines = markdown_content.split('\n')
                    source_lines = [line + '\n' for line in lines[:-1]]
                    if lines[-1]:
                        source_lines.append(lines[-1])
                    
                    notebook["cells"].append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": source_lines
                    })
            elif i % 3 == 1:  # Language identifier
                lang = parts[i] or 'python'
                code = parts[i + 1]
                
                if lang in ['python', 'py']:
                    # Split code into lines for notebook format, preserving newlines
                    lines = code.split('\n')
                    # Add newline to all lines except the last one
                    source_lines = [line + '\n' for line in lines[:-1]]
                    if lines[-1]:  # If last line is not empty, add it without newline
                        source_lines.append(lines[-1])
                    
                    notebook["cells"].append({
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": source_lines
                    })
                elif lang == 'bash':
                    # For bash blocks, add them as code cells with ! prefix
                    lines = code.split('\n')
                    source_lines = []
                    for line in lines[:-1]:
                        if line.strip():
                            source_lines.append('!' + line + '\n')
                        else:
                            source_lines.append('\n')
                    if lines[-1]:
                        source_lines.append('!' + lines[-1])
                    
                    notebook["cells"].append({
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": source_lines
                    })
                # Skip i+1 since we already processed the code
                i += 1
            i += 1
        
        return notebook