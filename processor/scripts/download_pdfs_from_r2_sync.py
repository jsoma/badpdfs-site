#!/usr/bin/env python3
"""
Sync PDFs from R2 storage - rsync-style approach.

Lists all PDFs in R2 and downloads any that are missing locally.
"""

import os
import sys
import boto3
import urllib.request
from pathlib import Path
from botocore.config import Config

def sync_pdfs_from_r2():
    """Sync PDFs from R2 using an rsync-like approach."""
    r2_endpoint = "https://abcc0a833279dafb69a331624d39a467.r2.cloudflarestorage.com"
    r2_public_url = os.environ.get('R2_PUBLIC_URL', 'https://pub-4e99d31d19cb404d8d4f5f7efa51ef6e.r2.dev')
    content_dir = Path(__file__).parent.parent.parent / 'content' / 'pdfs'
    
    downloaded = 0
    skipped = 0
    failed = 0
    
    # Try boto3 approach if credentials are available
    if os.environ.get('R2_ACCESS_KEY_ID'):
        print("Using boto3 to list R2 bucket contents...")
        try:
            # Create R2 client
            client = boto3.client(
                "s3",
                endpoint_url=r2_endpoint,
                aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
                region_name="auto",
                config=Config(signature_version='s3v4')
            )
            
            # List all objects under pdfs/
            paginator = client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket='badpdfs-gallery', Prefix='pdfs/'):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        if key.endswith('.pdf'):
                            # Extract path components
                            parts = key.split('/')
                            if len(parts) >= 3:  # pdfs/dir/file.pdf
                                pdf_dir_name = parts[1]
                                pdf_filename = parts[2]
                                
                                local_dir = content_dir / pdf_dir_name
                                local_path = local_dir / pdf_filename
                                
                                if local_path.exists():
                                    skipped += 1
                                else:
                                    local_dir.mkdir(exist_ok=True)
                                    print(f"Downloading {key}...")
                                    client.download_file('badpdfs-gallery', key, str(local_path))
                                    downloaded += 1
            
        except Exception as e:
            print(f"boto3 approach failed: {e}")
            print("Falling back to public URL approach...")
    
    # Fallback: scan local directories and try public URLs
    if not os.environ.get('R2_ACCESS_KEY_ID'):
        print("No R2 credentials found. Scanning local directories...")
        
        for pdf_dir in sorted(content_dir.iterdir()):
            if pdf_dir.is_dir() and pdf_dir.name != '.ipynb_checkpoints':
                # Check if directory has markdown files (indicates it should have PDFs)
                md_files = list(pdf_dir.glob('*.md'))
                if not md_files:
                    continue
                
                # Check if any PDFs already exist
                existing_pdfs = list(pdf_dir.glob('*.pdf'))
                if existing_pdfs:
                    skipped += len(existing_pdfs)
                    continue
                
                # Try to download using the default naming convention
                pdf_id = pdf_dir.name
                pdf_url = f"{r2_public_url}/pdfs/{pdf_id}/{pdf_id}.pdf"
                pdf_path = pdf_dir / f"{pdf_id}.pdf"
                
                print(f"Trying {pdf_url}...")
                try:
                    req = urllib.request.Request(pdf_url)
                    with urllib.request.urlopen(req) as response:
                        pdf_path.write_bytes(response.read())
                    downloaded += 1
                    print(f"✓ Downloaded {pdf_id}.pdf")
                except Exception as e:
                    # Can't know what the actual filename is without listing R2
                    print(f"⚠️  Could not download {pdf_id}: {e}")
                    print(f"   (Actual PDF filename in R2 might be different)")
                    failed += 1
                    # Create placeholder
                    pdf_path.write_bytes(b'%PDF-1.4\nPDF not available')
    
    print(f"\n📊 Summary: Downloaded {downloaded}, Skipped {skipped}, Failed {failed}")
    
    if failed > 0 and not os.environ.get('R2_ACCESS_KEY_ID'):
        print("\n💡 Tip: Set R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY environment variables")
        print("   to enable full rsync-style synchronization that handles any filename.")
    
    return 0

if __name__ == "__main__":
    sys.exit(sync_pdfs_from_r2())