#!/usr/bin/env python3
"""
Upload PDFs to Cloudflare R2 storage.

This is a standalone script that uploads PDFs from the content directory
to R2, using MD5 checksums to avoid re-uploading unchanged files.

Usage:
    python scripts/upload_to_r2.py              # Upload all PDFs
    python scripts/upload_to_r2.py --pdf focus  # Upload specific PDF
    python scripts/upload_to_r2.py --dry-run    # Show what would be uploaded
"""

import os
import sys
import json
import boto3
import hashlib
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import Config

# Load environment variables
load_dotenv()


class R2Uploader:
    """Handles uploading PDFs to Cloudflare R2."""
    
    def __init__(self):
        self.config = Config()
        
        # R2 Configuration
        self.r2_endpoint = "https://abcc0a833279dafb69a331624d39a467.r2.cloudflarestorage.com"
        self.r2_access_key_id = os.environ.get("R2_ACCESS_KEY_ID")
        self.r2_secret_access_key = os.environ.get("R2_SECRET_ACCESS_KEY")
        self.r2_bucket_name = "badpdfs-gallery"
        self.r2_public_url = "https://pub-4e99d31d19cb404d8d4f5f7efa51ef6e.r2.dev"
        
        # Statistics
        self.uploaded = 0
        self.skipped = 0
        self.failed = 0
    
    def validate_config(self) -> bool:
        """Check if R2 credentials are configured."""
        if not self.r2_access_key_id or not self.r2_secret_access_key:
            print("❌ R2 credentials not configured")
            print("   Set R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY environment variables")
            print("   Get these from Cloudflare Dashboard → R2 → Manage R2 API Tokens")
            return False
        return True
    
    def get_r2_client(self):
        """Create R2 client using boto3."""
        return boto3.client(
            "s3",
            endpoint_url=self.r2_endpoint,
            aws_access_key_id=self.r2_access_key_id,
            aws_secret_access_key=self.r2_secret_access_key,
            region_name="auto",  # R2 requires 'auto' as region
        )
    
    def calculate_md5(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file."""
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    
    def upload_pdf(self, pdf_path: Path, pdf_id: str, dry_run: bool = False) -> bool:
        """Upload a single PDF to R2."""
        if not pdf_path.exists():
            print(f"❌ PDF not found: {pdf_path}")
            self.failed += 1
            return False
        
        file_size = pdf_path.stat().st_size
        local_md5 = self.calculate_md5(pdf_path)
        
        # R2 key path - use the actual filename, not directory name
        key = f"pdfs/{pdf_id}/{pdf_path.name}"
        public_url = f"{self.r2_public_url}/{key}"
        
        if dry_run:
            print(f"Would upload: {key} ({file_size / 1024 / 1024:.1f} MB)")
            return True
        
        try:
            client = self.get_r2_client()
            
            # Check if file exists and get its ETag (MD5)
            needs_upload = True
            try:
                response = client.head_object(Bucket=self.r2_bucket_name, Key=key)
                remote_etag = response['ETag'].strip('"')
                
                if remote_etag == local_md5:
                    print(f"⏭️  {pdf_id}: unchanged (MD5 match)")
                    self.skipped += 1
                    needs_upload = False
            except client.exceptions.ClientError as e:
                if e.response['Error']['Code'] != '404':
                    raise
            
            if needs_upload:
                # Upload to R2
                with open(pdf_path, "rb") as f:
                    client.put_object(
                        Bucket=self.r2_bucket_name,
                        Key=key,
                        Body=f,
                        ContentType="application/pdf",
                    )
                
                print(f"✅ {pdf_id}: uploaded ({file_size / 1024 / 1024:.1f} MB)")
                self.uploaded += 1
            
            # Update metadata with size
            self._update_metadata(pdf_id, file_size)
            
            return True
            
        except Exception as e:
            print(f"❌ {pdf_id}: failed - {e}")
            self.failed += 1
            return False
    
    def _update_metadata(self, pdf_id: str, file_size: int):
        """Update metadata with PDF file size."""
        metadata_path = self.config.artifacts_dir / "pdfs" / pdf_id / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)
            
            metadata["pdf_size"] = file_size
            # Remove hardcoded URL if present
            metadata.pop("pdf_url", None)
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
    
    def upload_all(self, pdf_id: Optional[str] = None, dry_run: bool = False):
        """Upload all PDFs or a specific PDF."""
        print("🚀 R2 Upload Script")
        print("=" * 50)
        
        if not self.validate_config():
            return
        
        if dry_run:
            print("🔍 DRY RUN MODE - No files will be uploaded\n")
        
        # Get PDFs to process
        if pdf_id:
            # Upload specific PDF
            pdf_dirs = list(self.config.content_dir.glob(f"pdfs/{pdf_id}"))
            if not pdf_dirs:
                print(f"❌ PDF not found: {pdf_id}")
                return
            
            pdf_dir = pdf_dirs[0]
            for pdf_file in pdf_dir.glob("*.pdf"):
                self.upload_pdf(pdf_file, pdf_id, dry_run)
        else:
            # Upload all PDFs
            pdfs_dir = self.config.content_dir / "pdfs"
            if not pdfs_dir.exists():
                print(f"❌ PDFs directory not found: {pdfs_dir}")
                return
            
            for pdf_dir in sorted(pdfs_dir.iterdir()):
                if pdf_dir.is_dir():
                    pdf_id = pdf_dir.name
                    for pdf_file in pdf_dir.glob("*.pdf"):
                        self.upload_pdf(pdf_file, pdf_id, dry_run)
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Summary:")
        print(f"   Uploaded: {self.uploaded}")
        print(f"   Skipped:  {self.skipped}")
        print(f"   Failed:   {self.failed}")
        
        if self.failed > 0:
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Upload PDFs to Cloudflare R2 storage"
    )
    parser.add_argument(
        "--pdf",
        help="Upload a specific PDF by ID"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be uploaded without actually uploading"
    )
    
    args = parser.parse_args()
    
    uploader = R2Uploader()
    uploader.upload_all(pdf_id=args.pdf, dry_run=args.dry_run)


if __name__ == "__main__":
    main()