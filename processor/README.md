# PDF Gallery Processor

A sophisticated processing pipeline for the Bad PDFs Gallery that extracts metadata, executes code examples, generates screenshots, and builds search indices from markdown files documenting PDF extraction techniques.

## Architecture

The processor uses an object-oriented, task-based architecture:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Domain Models  │     │      Tasks      │     │      Core       │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ • PDFExample    │     │ • MetadataTask  │     │ • Processor     │
│ • Approach      │────▶│ • ExecutionTask │◀────│ • Cache         │
│ • Gallery       │     │ • ScreenshotTask│     │ • Config        │
└─────────────────┘     │ • SearchTask    │     └─────────────────┘
                        │ • ValidationTask│
                        │ • NotebookTask  │
                        └─────────────────┘
```

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run full build
python build.py build

# Process specific PDF
python build.py build --pdf example-pdf

# Check status
python build.py status

# Clean and rebuild
python build.py clean
python build.py rebuild
```

## Features

### 🎯 Smart Incremental Builds
- Only processes files that have changed
- Caches results at task level
- Tracks dependencies between tasks

### ☁️ R2 Upload Integration (New!)
- Automatic upload of PDFs to Cloudflare R2
- MD5-based deduplication (only uploads changed files)
- Optional - works without R2 credentials

### 📊 Comprehensive Processing
- **Metadata Extraction**: AST-based analysis of Python code
- **Code Execution**: Safe execution with output capture
- **Screenshot Generation**: PDF to PNG conversion with thumbnails
- **Search Index**: Full-text search with method indexing
- **Validation**: Ensures all artifacts are complete
- **Notebook Export**: Jupyter notebooks for Colab

### 🔧 Extensible Design
- Easy to add new tasks
- Plugin-friendly architecture
- Clear separation of concerns

## Configuration

Configuration is loaded from (in order):
1. `config.json` in project root
2. Environment variables
3. Default values

Example `config.json`:
```json
{
  "r2_public_url": "https://your-cdn.com",
  "screenshot_dpi": 150,
  "max_execution_time": 30,
  "verbose": false
}
```

## Tasks

### MetadataTask
Extracts YAML frontmatter and analyzes Python code to find:
- natural-pdf methods used
- CSS selectors
- Code complexity metrics

### ExecutionTask
Executes Python code blocks and captures:
- stdout/stderr output
- Matplotlib figures
- Rich outputs (DataFrames, etc.)

### ScreenshotTask
Generates PNG screenshots from PDFs:
- First N pages (configurable)
- Thumbnails for gallery view
- High-quality rendering

### SearchIndexTask
Builds search indices for frontend:
- Full-text search
- Method reverse index
- Search suggestions

### ValidationTask
Validates all artifacts:
- Checks required files exist
- Validates metadata completeness
- Creates valid_pdfs.json

### NotebookTask
Generates Jupyter notebooks:
- Includes installation instructions
- Downloads PDFs automatically
- Ready for Google Colab

## R2 Upload Script

PDFs can be uploaded to Cloudflare R2 storage using the standalone upload script:

### Setup

1. **Get R2 Credentials**:
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → R2
   - Create an R2 bucket named `badpdfs-gallery`
   - Go to "Manage R2 API Tokens" and create a token with read/write access

2. **Set Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your credentials:
   # R2_ACCESS_KEY_ID=your_key_id
   # R2_SECRET_ACCESS_KEY=your_secret_key
   ```

### Usage

```bash
# Upload all PDFs
python scripts/upload_to_r2.py

# Upload specific PDF
python scripts/upload_to_r2.py --pdf focus

# Dry run (see what would be uploaded)
python scripts/upload_to_r2.py --dry-run
```

The script:
- Uses MD5 checksums to skip unchanged files
- Updates metadata with file sizes
- Shows upload progress and statistics
- Runs independently from the build process

## Development

### Running Tests
```bash
pytest tests/
pytest tests/test_domain/  # Domain model tests
pytest tests/test_tasks/   # Task tests
```

### Adding a New Task
```python
from tasks import Task, TaskContext
from domain import PDFExample

class MyTask(Task):
    def __init__(self):
        super().__init__(name="my_task", dependencies=["metadata"])
    
    def process(self, pdf: PDFExample, context: TaskContext):
        # Your processing logic
        return {"status": "success"}
    
    def get_inputs(self, pdf: PDFExample):
        return [pdf.base_dir / "input.txt"]
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext):
        return [context.get_artifact_path(pdf, "output.json")]
```

### Cache Management

The build cache tracks:
- File hashes for change detection
- Task completion timestamps
- Task results for reuse

To inspect cache:
```python
from core import BuildCache
cache = BuildCache(Path(".build_cache.json"))
print(cache.get_stats())
```

## Migration from Old System

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions on migrating from the old script-based system.

## Troubleshooting

### Import Errors
Always run from the processor directory:
```bash
cd processor
source .venv/bin/activate
```

### Cache Issues
Clear cache and rebuild:
```bash
rm .build_cache.json
python build.py rebuild
```

### Memory Issues
For large galleries, process in batches:
```bash
python build.py build --pdf pdf1
python build.py build --pdf pdf2
```

## Performance

The new architecture provides:
- ⚡ 50%+ faster builds through smart caching
- 📈 Linear scaling with PDF count
- 💾 Minimal memory footprint
- 🔄 Resumable processing

## Future Enhancements

- [ ] Parallel task execution
- [ ] Web UI for monitoring
- [ ] Database backend
- [ ] Cloud processing support
- [ ] Real-time progress updates

## License

Part of the Bad PDFs Gallery project.