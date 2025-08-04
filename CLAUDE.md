# Bad PDFs Gallery Project

This project is building a gallery website to showcase natural-pdf library usage through real-world PDF extraction examples.

## Important Documents

**Read ARCHITECTURE.md first** - Contains all architecture decisions, structure, and implementation details for the gallery site.

## Project Overview

- Gallery of 200+ PDF extraction examples
- Each PDF has executable Python code showing extraction techniques
- Modern, colorful, bold design (not typical technical documentation)
- Focus on visual workflows with side-by-side code and outputs

## Key Features

- Toggle between card/list gallery views
- Search by natural-pdf methods used
- Multiple approach examples per PDF
- Topic pages (OCR, tables, forms)
- Export to Colab notebooks
- Auto-generated previews and metadata

## Development Guidelines

When working on this project:
1. Refer to ARCHITECTURE.md for all structural decisions
2. PDFs are stored on S3, not in the repository
3. Use the processor → artifacts → frontend pipeline
4. Keep Python processing separate from frontend code
5. Test markdown files in VSCode with Python extension

## Essential Commands

### Processing Pipeline (run from `/processor` directory)

**ALWAYS ACTIVATE THE VIRTUAL ENVIRONMENT FIRST:**
```bash
cd processor
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

**IMPORTANT: This project uses the local development version of natural-pdf:**
```bash
# If natural-pdf is not installed from local development:
pip install -e ~/Development/natural-pdf
```

**Full Processing Pipeline (Recommended):**
```bash
python build.py build
```
This intelligently rebuilds only what's changed. Use `python build.py rebuild` to force rebuild everything.

**Other build commands:**
```bash
python build.py status     # Check current build state
python build.py clean      # Remove all artifacts
python build.py build -v   # Verbose output
```

**Legacy full pipeline (rebuilds everything):**
```bash
python process_all.py
```

**Individual Processing Steps:**
```bash
# 1. Extract metadata from markdown files
python generate_artifacts.py

# 2. Execute Python code in markdown files
python execute_markdown.py ../content -v --install-deps

# 3. Generate PDF screenshots and thumbnails
python generate_screenshots.py ../content/pdfs --thumbnails --thumbnail-size 400 400 -v

# 4. Build search index for frontend
python generate_search_index.py

# 5. Validate artifacts and create valid_pdfs.json
python validate_artifacts.py
```

### Frontend (run from `/frontend` directory)

**Development Server:**
```bash
cd frontend
npm run dev
# Server runs at http://localhost:4321
```

**Build for Production:**
```bash
npm run build
npm run preview  # Test production build locally
```

## Common Issues & Solutions

### "ENOENT: no such file or directory, open '.../artifacts/valid_pdfs.json'"
Run the full processor pipeline: `cd processor && source .venv/bin/activate && python process_all.py`

### Method URLs returning 404 (e.g., /methods/PDF())
The processor was updated to remove parentheses from method names. Re-run: `python process_all.py`

### Changes to Python processing not reflected
Always run from the processor directory with .venv activated:
```bash
cd processor
source ./bin/activate
python process_all.py
```

## Project Structure

```
/
├── processor/          # Python processing pipeline
│   ├── .venv/          # Virtual environment (ALWAYS USE THIS)
│   └── *.py           # Processing scripts
├── frontend/          # Astro.js frontend
│   ├── src/
│   └── public/artifacts/  # Generated data from processor
└── content/           # Source markdown files
    └── pdfs/         # PDF examples
```

## Key Files Modified Recently

- `processor/src/metadata_extractor.py` - Fixed method name extraction (removed parentheses)
- `frontend/src/styles/global.css` - Added shared `.method-tag` and `.tag-tag` styles
- `frontend/src/pages/pdfs/[slug].astro` - Updated to use consistent tag styling
- `frontend/src/components/Search.astro` - Fixed gradient text issue on `.method-name`

## Development Memories

- Do not run the server yourself, always ask the user to run the server
- After front-end changes, check the website with playwright to confirm it works. Click, take screenshots, etc, whatever is necessary.
- Methods should be displayed consistently across all pages (home, PDF detail, search)
- Tag/method badges use vibrant colors but professional styling (no crazy gradients)