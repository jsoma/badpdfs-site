"""
Incremental validation task for PDF Gallery.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Set

from domain import PDFExample
from tasks import Task, TaskContext


class IncrementalValidationTask(Task):
    """
    Task to validate PDFs and incrementally update valid_pdfs.json and all_metadata.json.
    
    This task:
    - Validates individual PDFs
    - Updates existing metadata files incrementally
    - Maintains compatibility with batch operations
    """
    
    def __init__(self):
        super().__init__(
            name="incremental_validation", 
            dependencies=["metadata", "execution", "screenshots"]
        )
    
    def process(self, pdf: PDFExample, context: TaskContext) -> Dict[str, Any]:
        """Validate a single PDF and update the aggregate files."""
        if not pdf.is_published():
            context.log(f"Skipping unpublished PDF: {pdf.id}", "INFO")
            return {"status": "skipped", "reason": "unpublished"}
        
        # Load existing metadata files
        all_metadata_path = context.artifacts_dir / "all_metadata.json"
        valid_pdfs_path = context.artifacts_dir / "valid_pdfs.json"
        
        # Load existing data or initialize empty
        if all_metadata_path.exists():
            all_metadata = context.read_artifact(all_metadata_path)
        else:
            all_metadata = []
        
        if valid_pdfs_path.exists():
            valid_pdf_ids = set(context.read_artifact(valid_pdfs_path))
        else:
            valid_pdf_ids = set()
        
        # Remove any existing entries for this PDF
        all_metadata = [m for m in all_metadata if m.get('id') != pdf.id]
        valid_pdf_ids.discard(pdf.id)
        
        # Load metadata for validation
        metadata_path = context.get_artifact_path(pdf, "metadata.json")
        if not metadata_path.exists():
            context.log(f"No metadata found for {pdf.id}", "ERROR")
            return {
                "status": "invalid",
                "errors": ["missing_metadata"]
            }
        
        metadata_list = context.read_artifact(metadata_path)
        valid_approaches = []
        invalid_approaches = []
        
        # Validate each approach
        for metadata in metadata_list:
            errors = self._validate_approach(pdf, metadata, context)
            
            if errors:
                invalid_approaches.append({
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
                valid_approaches.append(metadata)
                all_metadata.append(metadata)
                context.log(f"✓ {pdf.id}/{metadata['slug']} validated", "SUCCESS")
        
        # Update valid_pdfs if at least one approach is valid
        if valid_approaches:
            valid_pdf_ids.add(pdf.id)
        
        # Sort metadata by slug for consistent ordering
        all_metadata.sort(key=lambda x: x.get('slug', ''))
        
        # Save updated files
        context.write_artifact(all_metadata_path, all_metadata)
        context.write_artifact(valid_pdfs_path, sorted(list(valid_pdf_ids)))
        
        # Update validation report incrementally
        self._update_validation_report(
            context, pdf.id, valid_approaches, invalid_approaches
        )
        
        # Update summary
        self._update_summary(context, all_metadata, valid_pdf_ids)
        
        return {
            "status": "valid" if valid_approaches else "invalid",
            "valid_count": len(valid_approaches),
            "invalid_count": len(invalid_approaches)
        }
    
    def _update_validation_report(self, context: TaskContext, pdf_id: str, 
                                  valid_approaches: List[Dict], 
                                  invalid_approaches: List[Dict]):
        """Update the validation report incrementally."""
        report_path = context.artifacts_dir / "validation_report.json"
        
        if report_path.exists():
            report = context.read_artifact(report_path)
        else:
            report = {
                "total_items": 0,
                "valid_count": 0,
                "invalid_count": 0,
                "valid_pdf_ids": [],
                "invalid_items": []
            }
        
        # Remove old entries for this PDF
        report["invalid_items"] = [
            item for item in report.get("invalid_items", [])
            if item.get("item", {}).get("id") != pdf_id
        ]
        
        # Add new invalid items
        for invalid in invalid_approaches:
            report["invalid_items"].append(invalid)
        
        # Recalculate counts
        all_metadata_path = context.artifacts_dir / "all_metadata.json"
        if all_metadata_path.exists():
            all_metadata = context.read_artifact(all_metadata_path)
            report["valid_count"] = len(all_metadata)
        
        report["invalid_count"] = len(report["invalid_items"])
        report["total_items"] = report["valid_count"] + report["invalid_count"]
        
        # Update valid PDF IDs
        valid_pdfs_path = context.artifacts_dir / "valid_pdfs.json"
        if valid_pdfs_path.exists():
            report["valid_pdf_ids"] = context.read_artifact(valid_pdfs_path)
        
        context.write_artifact(report_path, report)
    
    def _update_summary(self, context: TaskContext, all_metadata: List[Dict], 
                       valid_pdf_ids: Set[str]):
        """Update summary statistics."""
        summary_path = context.artifacts_dir / "summary.json"
        
        # Count total published PDFs in the gallery
        from domain import Gallery
        from pathlib import Path
        
        # Get paths from context
        content_dir = Path(context.artifacts_dir).parent / "content"
        gallery = Gallery(
            content_dir=content_dir,
            artifacts_dir=context.artifacts_dir
        )
        total_published = sum(1 for p in gallery.pdfs if p.is_published())
        
        summary = {
            "total_pdfs": len(gallery.pdfs),
            "published_pdfs": total_published,
            "valid_approaches": len(all_metadata),
            "valid_pdfs": len(valid_pdf_ids),
            "invalid_approaches": 0  # Will be updated from report
        }
        
        # Get invalid count from report
        report_path = context.artifacts_dir / "validation_report.json"
        if report_path.exists():
            report = context.read_artifact(report_path)
            summary["invalid_approaches"] = report.get("invalid_count", 0)
        
        context.write_artifact(summary_path, summary)
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Input files for validation."""
        # Since we don't have context here, return empty list
        # The actual paths are checked in the process method
        return []
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files - these are shared across all PDFs."""
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
                                "details": exec_result.get('error', 'Unknown error')
                            })
                            break  # Only report first error
        
        # Check method usage
        if not metadata.get('methods'):
            errors.append({
                "type": "no_methods",
                "message": "No natural-pdf methods detected"
            })
        
        return errors