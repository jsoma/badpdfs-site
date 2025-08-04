"""
Screenshot generation task for PDF Gallery.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

from domain import PDFExample
from tasks import Task, TaskContext

# Try to import pdf2image
try:
    from pdf2image import convert_from_path
    HAS_PDF2IMAGE = True
except ImportError:
    HAS_PDF2IMAGE = False
    convert_from_path = None

# Try to import PIL
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    Image = None


logger = logging.getLogger(__name__)


class ScreenshotTask(Task):
    """
    Task to generate screenshots from PDF files.
    
    This includes:
    - Converting PDF pages to PNG images
    - Generating thumbnails
    - Handling multi-page PDFs
    """
    
    def __init__(self, 
                 max_pages: int = 10,
                 dpi: int = 150,
                 thumbnail_size: Tuple[int, int] = (400, 400)):
        super().__init__(name="screenshots", dependencies=[])
        self.max_pages = max_pages
        self.dpi = dpi
        self.thumbnail_size = thumbnail_size
        
        if not HAS_PDF2IMAGE:
            logger.warning("pdf2image not installed. PDF screenshots will not be available.")
        if not HAS_PIL:
            logger.warning("PIL/Pillow not installed. Image operations will be limited.")
    
    def process(self, pdf: PDFExample, context: TaskContext) -> Dict[str, Any]:
        """Generate screenshots for a PDF."""
        if not HAS_PDF2IMAGE:
            context.log(f"Skipping {pdf.id}: pdf2image not installed", "SKIP")
            return {"status": "skipped", "reason": "pdf2image not installed"}
        
        # Get primary PDF file
        pdf_file = pdf.get_primary_pdf()
        if not pdf_file:
            context.log(f"No PDF file found for {pdf.id}", "ERROR")
            return {"status": "error", "reason": "No PDF file found"}
        
        context.log(f"Generating screenshots for {pdf_file.name}")
        
        try:
            # Generate screenshots
            result = self._generate_screenshots(pdf_file, pdf, context)
            
            return {
                "status": "success",
                "pdf_file": pdf_file.name,
                "page_count": result['page_count'],
                "screenshots_generated": len(result['screenshots'])
            }
            
        except Exception as e:
            context.log(f"Error generating screenshots for {pdf.id}: {e}", "ERROR")
            return {
                "status": "error",
                "reason": str(e)
            }
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Input files are PDF files."""
        return pdf.pdf_files
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files are screenshot images."""
        outputs = []
        screenshots_dir = context.artifacts_dir / "screenshots" / pdf.id
        
        # We can't know exact outputs without processing, so check if directory exists
        if screenshots_dir.exists():
            outputs.extend(screenshots_dir.glob("*.png"))
        else:
            # Estimate outputs based on PDF file
            pdf_file = pdf.get_primary_pdf()
            if pdf_file:
                # At minimum, first page screenshot
                outputs.append(screenshots_dir / f"{pdf_file.stem}-1.png")
        
        return outputs
    
    def _get_resample_filter(self):
        """Get appropriate resample filter for PIL."""
        if HAS_PIL and hasattr(Image, 'Resampling'):
            return Image.Resampling.LANCZOS
        elif HAS_PIL:
            return Image.LANCZOS
        return None
    
    def _generate_screenshots(self, pdf_path: Path, pdf: PDFExample, 
                            context: TaskContext) -> Dict[str, Any]:
        """Generate screenshots from a PDF file."""
        result = {
            'pdf_path': str(pdf_path),
            'page_count': 0,
            'screenshots': []
        }
        
        # Convert PDF to images
        try:
            # Get page count with low DPI first
            all_pages = convert_from_path(pdf_path, dpi=72, fmt='jpeg')
            result['page_count'] = len(all_pages)
            
            # Convert pages with high quality
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=1,
                last_page=min(self.max_pages, len(all_pages)),
                fmt='png',
                use_pdftocairo=True  # Better rendering if available
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF: {e}")
        
        # Save screenshots
        screenshots_dir = context.artifacts_dir / "screenshots" / pdf.id
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        for i, image in enumerate(images):
            page_num = i + 1
            
            # Main screenshot path
            img_path = screenshots_dir / f"{pdf_path.stem}-{page_num}.png"
            
            # Save main screenshot
            image.save(str(img_path), 'PNG')
            
            screenshot_info = {
                'page': page_num,
                'file_path': str(img_path.relative_to(context.artifacts_dir)),
                'width': image.size[0],
                'height': image.size[1]
            }
            
            # Generate thumbnail
            if HAS_PIL and self.thumbnail_size:
                thumb_path = screenshots_dir / f"{pdf_path.stem}-{page_num}-thumb.png"
                thumb = image.copy()
                thumb.thumbnail(self.thumbnail_size, self._get_resample_filter())
                thumb.save(str(thumb_path), 'PNG')
                screenshot_info['thumbnail_path'] = str(
                    thumb_path.relative_to(context.artifacts_dir)
                )
            
            result['screenshots'].append(screenshot_info)
        
        return result
    
    def needs_processing(self, pdf: PDFExample, context: TaskContext) -> bool:
        """
        Check if screenshots need to be generated.
        
        Override base implementation to be smarter about checking.
        """
        # First check if any PDF files changed
        for pdf_file in self.get_inputs(pdf):
            if context.cache.has_file_changed(pdf_file):
                return True
        
        # Check if screenshots directory exists
        screenshots_dir = context.artifacts_dir / "screenshots" / pdf.id
        if not screenshots_dir.exists():
            return True
        
        # Check if we have at least one screenshot
        screenshots = list(screenshots_dir.glob("*.png"))
        if not screenshots:
            return True
        
        # If we have screenshots and PDFs haven't changed, we're good
        return False