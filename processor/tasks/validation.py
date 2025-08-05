"""
Validation task for PDF Gallery.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

from domain import PDFExample
from tasks import BatchTask, TaskContext


class ValidationTask(BatchTask):
    """
    Task to validate all artifacts and create valid_pdfs.json.
    
    This is a batch task that:
    - Checks all required artifacts exist
    - Validates metadata completeness
    - Creates a list of valid PDFs for the frontend
    """
    
    def __init__(self):
        super().__init__(
            name="validation", 
            dependencies=["metadata", "execution", "screenshots", "search_index"]
        )
    
    def process_batch(self, pdfs: List[PDFExample], context: TaskContext) -> Dict[str, Any]:
        """Validate all PDFs and their artifacts."""
        valid_items = []
        invalid_items = []
        all_metadata = []
        
        # Validate each PDF
        for pdf in pdfs:
            if not pdf.is_published():
                continue
            
            # Load metadata for validation
            metadata_path = context.get_artifact_path(pdf, "metadata.json")
            if not metadata_path.exists():
                invalid_items.append({
                    "id": pdf.id,
                    "errors": [{
                        "type": "missing_metadata",
                        "message": "No metadata file found"
                    }]
                })
                continue
            
            metadata_list = context.read_artifact(metadata_path)
            
            # Validate each approach
            for metadata in metadata_list:
                errors = self._validate_approach(pdf, metadata, context)
                
                # Add ALL metadata to all_metadata, not just valid ones
                all_metadata.append(metadata)
                
                if errors:
                    invalid_items.append({
                        "item": metadata,
                        "errors": errors
                    })
                    context.log(
                        f"Validation failed for {pdf.id}/{metadata['slug']}: {len(errors)} errors",
                        "ERROR"
                    )
                    for error in errors:
                        context.log(f"  - {error['type']}: {error['message']}", "ERROR")
                else:
                    valid_items.append(metadata)
                    context.log(f"✓ {pdf.id}/{metadata['slug']} validated", "SUCCESS")
        
        # Save all_metadata.json (combining ALL approaches, valid and invalid)
        all_metadata_path = context.artifacts_dir / "all_metadata.json"
        context.write_artifact(all_metadata_path, all_metadata)
        
        # Create valid_pdfs.json (list of valid PDF IDs)
        valid_pdf_ids = list(set(item['id'] for item in valid_items))
        valid_pdfs_path = context.artifacts_dir / "valid_pdfs.json"
        context.write_artifact(valid_pdfs_path, sorted(valid_pdf_ids))
        
        # Save validation report
        report = {
            "total_items": len(valid_items) + len(invalid_items),
            "valid_count": len(valid_items),
            "invalid_count": len(invalid_items),
            "valid_pdf_ids": valid_pdf_ids,
            "invalid_items": invalid_items
        }
        
        report_path = context.artifacts_dir / "validation_report.json"
        context.write_artifact(report_path, report)
        
        # Summary statistics
        summary = {
            "total_pdfs": len(pdfs),
            "published_pdfs": sum(1 for p in pdfs if p.is_published()),
            "valid_approaches": len(valid_items),
            "valid_pdfs": len(valid_pdf_ids),
            "invalid_approaches": len(invalid_items)
        }
        
        summary_path = context.artifacts_dir / "summary.json"
        context.write_artifact(summary_path, summary)
        
        return {
            "valid_count": len(valid_items),
            "invalid_count": len(invalid_items),
            "valid_pdf_count": len(valid_pdf_ids)
        }
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Inputs are all generated artifacts."""
        # Note: This is called per-PDF but we're a batch task
        return []
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files - not used for batch tasks."""
        # BatchTask doesn't use per-PDF outputs
        return []
    
    def get_batch_outputs(self, context: TaskContext) -> List[Path]:
        """Output files for validation."""
        return [
            context.artifacts_dir / "all_metadata.json",
            context.artifacts_dir / "valid_pdfs.json",
            context.artifacts_dir / "validation_report.json",
            context.artifacts_dir / "summary.json"
        ]
    
    def _validate_approach(self, pdf: PDFExample, metadata: Dict[str, Any], 
                          context: TaskContext) -> List[Dict[str, Any]]:
        """Validate a single approach."""
        errors = []
        slug = metadata.get('slug', 'unknown')
        
        # Check required metadata fields
        required_fields = ['id', 'title', 'slug', 'pdf']
        for field in required_fields:
            if field not in metadata or not metadata[field]:
                errors.append({
                    "type": "missing_field",
                    "field": field,
                    "message": f"Required field '{field}' is missing or empty"
                })
        
        # Check if PDF file exists
        if 'pdf' in metadata:
            pdf_name = metadata['pdf']
            pdf_file = pdf.base_dir / pdf_name
            
            if not pdf_file.exists():
                errors.append({
                    "type": "missing_pdf",
                    "file": pdf_name,
                    "message": f"PDF file not found: {pdf_file}"
                })
        
        # Check screenshots
        screenshot_dir = context.artifacts_dir / "screenshots" / pdf.id
        if not screenshot_dir.exists():
            errors.append({
                "type": "missing_screenshots",
                "message": "No screenshot directory found"
            })
        else:
            # Check for at least one screenshot
            screenshots = list(screenshot_dir.glob("*.png"))
            if not screenshots:
                errors.append({
                    "type": "no_screenshots",
                    "message": "Screenshot directory exists but contains no images"
                })
            else:
                # Check for first page screenshot
                pdf_stem = metadata.get('pdf', 'unknown').replace('.pdf', '')
                expected_screenshot = screenshot_dir / f"{pdf_stem}-1.png"
                if not expected_screenshot.exists():
                    errors.append({
                        "type": "missing_main_screenshot",
                        "message": f"Expected screenshot not found: {expected_screenshot.name}"
                    })
        
        # Check execution results
        exec_path = context.get_artifact_path(pdf, "executions", f"{slug}.json")
        if not exec_path.exists():
            errors.append({
                "type": "missing_execution",
                "message": f"No execution results found for {slug}"
            })
        else:
            # Check if execution has errors
            execution = context.read_artifact(exec_path)
            if execution:
                for cell in execution.get('cells', []):
                    if cell.get('type') == 'code':
                        exec_result = cell.get('execution', {})
                        if exec_result.get('status') == 'error':
                            errors.append({
                                "type": "execution_error",
                                "message": "Code execution failed",
                                "details": exec_result.get('error', 'Unknown error'),
                                "code": cell.get('content', 'Code not available')
                            })
                            break  # Only report first error
        
        # Check method usage
        if not metadata.get('methods'):
            errors.append({
                "type": "no_methods",
                "message": "No natural-pdf methods detected"
            })
        
        return errors