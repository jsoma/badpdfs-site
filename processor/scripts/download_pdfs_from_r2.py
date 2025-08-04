#!/usr/bin/env python3
"""
Download PDFs from R2 storage for CI/CD builds.

This script downloads PDFs that aren't already cached, creating
placeholder files for any that are missing from R2.
"""

import os
import sys
import json
import urllib.request
from pathlib import Path

def download_pdfs():
    """Download PDFs from R2, skipping cached ones."""
    r2_base = os.environ.get('R2_PUBLIC_URL', 'https://pub-4e99d31d19cb404d8d4f5f7efa51ef6e.r2.dev')
    content_dir = Path(__file__).parent.parent.parent / 'content' / 'pdfs'
    
    downloaded = 0
    skipped = 0
    failed = 0
    failed_pdfs = []
    
    # Special case mappings for PDFs with different names
    pdf_name_overrides = {
        'ocr-example': 'needs-ocr.pdf',
        'simple-text': 'practice.pdf',
        'multicolumn-layout': 'multicolumn.pdf',
        'inspection-form': 'practice.pdf',
        'example-tabs': 'example-tabs.pdf',  # Might need adjustment
        'cia-document': 'cia-doc.pdf'  # Common abbreviation
    }
    
    # Read all PDF directories
    for pdf_dir in sorted(content_dir.iterdir()):
        if pdf_dir.is_dir() and pdf_dir.name != '.ipynb_checkpoints':
            md_files = list(pdf_dir.glob('*.md'))
            if md_files:
                pdf_id = pdf_dir.name
                
                # Check for existing PDFs in the directory
                existing_pdfs = list(pdf_dir.glob('*.pdf'))
                if existing_pdfs:
                    skipped += len(existing_pdfs)
                    continue
                
                # Determine the PDF filename to download
                if pdf_id in pdf_name_overrides:
                    pdf_filename = pdf_name_overrides[pdf_id]
                else:
                    pdf_filename = f"{pdf_id}.pdf"
                
                pdf_url = f"{r2_base}/pdfs/{pdf_id}/{pdf_filename}"
                pdf_path = pdf_dir / pdf_filename
                
                print(f"Downloading {pdf_id}/{pdf_filename}...")
                try:
                    # Try to download with a user agent header
                    req = urllib.request.Request(
                        pdf_url,
                        headers={'User-Agent': 'Mozilla/5.0 (compatible; BadPDFs/1.0)'}
                    )
                    with urllib.request.urlopen(req) as response:
                        pdf_path.write_bytes(response.read())
                    downloaded += 1
                except Exception as e:
                    # If override didn't work, try default name
                    if pdf_id in pdf_name_overrides:
                        try:
                            default_url = f"{r2_base}/pdfs/{pdf_id}/{pdf_id}.pdf"
                            req = urllib.request.Request(
                                default_url,
                                headers={'User-Agent': 'Mozilla/5.0 (compatible; BadPDFs/1.0)'}
                            )
                            with urllib.request.urlopen(req) as response:
                                (pdf_dir / f"{pdf_id}.pdf").write_bytes(response.read())
                            downloaded += 1
                            print(f"  ✓ Downloaded using default name instead")
                        except:
                            print(f"⚠️  Could not download {pdf_id}: {e}")
                            failed += 1
                            failed_pdfs.append(pdf_id)
                            # Create a placeholder PDF
                            pdf_path.write_bytes(b'%PDF-1.4\nPDF not available')
                    else:
                        print(f"⚠️  Could not download {pdf_id}: {e}")
                        failed += 1
                        failed_pdfs.append(pdf_id)
                        # Create a placeholder PDF
                        pdf_path.write_bytes(b'%PDF-1.4\nPDF not available')
    
    print(f"\n📊 Summary: Downloaded {downloaded}, Skipped {skipped} (cached), Failed {failed}")
    
    if failed > 0:
        print(f"\n⚠️  WARNING: {failed} PDFs are not available on R2")
        print("These PDFs need to be uploaded locally using:")
        print("  python scripts/upload_to_r2.py")
        print("\nThe build will continue, but these PDFs will be missing from the site.")
        
        # Save manifest of missing PDFs
        manifest_path = Path(__file__).parent.parent / 'missing_pdfs.json'
        with open(manifest_path, 'w') as f:
            json.dump({
                'missing_count': failed,
                'missing_pdfs': failed_pdfs
            }, f, indent=2)
    
    return 0  # Don't fail the build

if __name__ == "__main__":
    sys.exit(download_pdfs())