#!/usr/bin/env python3
"""
Generate a static HTML dashboard for managing PDFs.

This is a standalone script that can be run independently of the build system.
"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core import Config
from tasks import DashboardTask, TaskContext
from domain import Gallery

def generate_dashboard():
    """Generate a static HTML dashboard with embedded metadata."""
    
    # Initialize configuration
    config = Config()
    
    # Create minimal context
    context = TaskContext(
        artifacts_dir=config.artifacts_dir,
        config=config.to_dict(),
        cache=None,  # Not needed for dashboard
        results={},
        verbose=True
    )
    
    # Initialize gallery to get PDFs
    gallery = Gallery(
        content_dir=config.content_dir,
        artifacts_dir=config.artifacts_dir
    )
    
    # Get all PDFs (published and unpublished)
    all_pdfs = list(gallery.examples.values())
    
    # Create and run dashboard task
    dashboard_task = DashboardTask()
    
    try:
        result = dashboard_task.process_batch(all_pdfs, context)
        
        if 'dashboard_path' in result:
            dashboard_path = Path(result['dashboard_path'])
            print(f"✅ Generated dashboard: {dashboard_path}")
            print(f"   Open with: file://{dashboard_path.absolute()}")
            print(f"\n📊 Statistics:")
            print(f"   Total PDFs: {result['total_pdfs']}")
            print(f"   Published: {result['published']}")
            print(f"   Unpublished: {result['unpublished']}")
            print(f"\n💡 To open files in VS Code, the links use vscode:// protocol.")
            print("   If they don't work, you may need to install the VS Code command line tools.")
        else:
            print("❌ Dashboard generation failed")
            
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_dashboard()