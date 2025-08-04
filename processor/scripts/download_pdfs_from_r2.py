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
    
    # Read all PDF directories
    for pdf_dir in sorted(content_dir.iterdir()):
        if pdf_dir.is_dir() and pdf_dir.name != '.ipynb_checkpoints':
            md_files = list(pdf_dir.glob('*.md'))
            if md_files:
                pdf_id = pdf_dir.name
                pdf_url = f"{r2_base}/pdfs/{pdf_id}/{pdf_id}.pdf"
                pdf_path = pdf_dir / f"{pdf_id}.pdf"
                
                if not pdf_path.exists():
                    print(f"Downloading {pdf_id}...")
                    try:
                        urllib.request.urlretrieve(pdf_url, pdf_path)
                        downloaded += 1
                    except Exception as e:
                        print(f"⚠️  Could not download {pdf_id}: {e}")
                        failed += 1
                        failed_pdfs.append(pdf_id)
                        # Create a placeholder PDF so build can continue
                        pdf_path.write_bytes(b'%PDF-1.4\nPDF not available')
                else:
                    skipped += 1
    
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