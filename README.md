# Bad PDFs Gallery

A gallery showcasing real-world PDF extraction examples using the natural-pdf library. Each PDF demonstrates different extraction techniques with executable Python code.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Access to natural-pdf library
- (Optional) R2 credentials for PDF hosting

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/badpdfs-analysis.git
cd badpdfs-analysis

# Set up Python environment
cd processor
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
pip install -e ~/Development/natural-pdf  # Or your natural-pdf location

# Build artifacts
python build.py build

# Start frontend development server
cd ../frontend
npm install
npm run dev
# Visit http://localhost:4321
```

## 📄 Adding or Updating PDFs

### Step 1: Create Markdown File

Create a new directory and markdown file in `content/pdfs/`:

```bash
content/pdfs/
└── my-example-pdf/
    └── my-example-pdf.md
```

The markdown file should contain:

```markdown
---
title: "My Example PDF"
description: "Description of what this PDF demonstrates"
approach: "ai"  # or "selectors", "hybrid", "coordinates"
methods:
  - PDF
  - extract_structured_data
  - content
tags:
  - forms
  - tables
difficulty: intermediate
pdf_url: "https://pub-4e99d31d19cb404d8d4f5f7efa51ef6e.r2.dev/pdfs/my-example-pdf/my-example-pdf.pdf"
---

# My Example PDF

This PDF demonstrates...

```python
pdf = PDF("my-example-pdf.pdf")
result = pdf.extract_structured_data(...)
print(result)
```
```

### Step 2: Upload PDF to R2

Place your PDF in the same directory:

```bash
content/pdfs/my-example-pdf/my-example-pdf.pdf
```

Upload to R2 storage:

```bash
cd processor
source .venv/bin/activate

# Set R2 credentials (one time)
export R2_ACCESS_KEY_ID="your_key"
export R2_SECRET_ACCESS_KEY="your_secret"

# Upload the PDF
python scripts/upload_to_r2.py --pdf my-example-pdf

# Or upload all PDFs
python scripts/upload_to_r2.py
```

### Step 3: Test Locally

```bash
# Process the new PDF
cd processor
python build.py build --pdf my-example-pdf

# Verify it works
cd ../frontend
npm run dev
```

### Step 4: Push to GitHub

```bash
git add content/pdfs/my-example-pdf/
git commit -m "Add my-example-pdf extraction example"
git push origin main
```

The GitHub Actions workflow will automatically build and deploy your changes.

## 🏗️ Architecture

### Directory Structure

```
badpdfs-analysis/
├── content/
│   └── pdfs/          # PDF examples (markdown files)
├── processor/         # Python processing pipeline
│   ├── core/          # Core functionality
│   ├── domain/        # Domain models
│   ├── tasks/         # Processing tasks
│   └── scripts/       # Utility scripts
├── frontend/          # Astro.js website
│   └── public/
│       └── artifacts/ # Generated data
└── .github/
    └── workflows/     # CI/CD pipelines
```

### Processing Pipeline

1. **Metadata Extraction**: Parses YAML frontmatter and analyzes Python code
2. **Code Execution**: Runs Python examples and captures output
3. **Screenshot Generation**: Creates PDF thumbnails and previews
4. **Search Index**: Builds searchable index of methods and content
5. **Validation**: Ensures all artifacts are complete
6. **Frontend Sync**: Copies artifacts to frontend

### Build System

The processor uses an intelligent caching system:

- Only processes files that have changed
- Caches results at task level
- Tracks dependencies between tasks

```bash
# Full build
python build.py build

# Build specific PDF
python build.py build --pdf example-pdf

# Check build status
python build.py status

# Clean all artifacts
python build.py clean
```

## 🚀 Deployment

The site automatically deploys to GitHub Pages when you push to main.

### First Time Setup

1. **Update GitHub Actions workflow** (`/.github/workflows/deploy.yml`):
   ```yaml
   # Line 68: Update with your natural-pdf repo
   pip install git+https://github.com/YOUR_USERNAME/natural-pdf.git
   ```

2. **Update Astro config** (`frontend/astro.config.mjs`):
   ```javascript
   base: '/YOUR_REPO_NAME/',  // Must match GitHub repo name
   site: 'https://YOUR_USERNAME.github.io',
   ```

3. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` / `/ (root)`

### Deployment Process

1. Push changes to `main` branch
2. GitHub Actions workflow:
   - Downloads PDFs from R2 (public URL)
   - Builds processor artifacts (with caching)
   - Builds frontend
   - Deploys to `gh-pages` branch
3. Site updates at `https://username.github.io/repo-name/`

## 🔧 Configuration

### R2 Storage Setup

1. Create Cloudflare R2 bucket named `badpdfs-gallery`
2. Create R2 API token with read/write access
3. Set environment variables:
   ```bash
   export R2_ACCESS_KEY_ID="your_key"
   export R2_SECRET_ACCESS_KEY="your_secret"
   ```

### Local Configuration

Create `config.json` in project root:

```json
{
  "r2_public_url": "https://pub-4e99d31d19cb404d8d4f5f7efa51ef6e.r2.dev",
  "screenshot_dpi": 150,
  "max_execution_time": 30,
  "verbose": true
}
```

## 🛠️ Troubleshooting

### Import Errors

Always run from the processor directory:
```bash
cd processor
source .venv/bin/activate
```

### Missing PDFs

Check if PDFs are on R2:
```bash
python scripts/upload_to_r2.py --dry-run
```

### Build Cache Issues

Clear cache and rebuild:
```bash
rm .build_cache.json
python build.py rebuild
```

### Frontend Not Updating

Ensure artifacts are synced:
```bash
python build.py build
# This automatically syncs to frontend/public/artifacts/
```

## 📚 Writing Good Examples

1. **Keep code focused** on the specific extraction technique
2. **Show the output** using print statements
3. **Handle errors** gracefully with try/except blocks
4. **Add comments** explaining non-obvious steps
5. **Use consistent formatting** for better readability

Example:

```python
# Extract data from a complex form
pdf = PDF("form-example.pdf")

# Method 1: AI extraction
try:
    data = pdf.extract_structured_data(
        description="Extract all form fields and their values"
    )
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"AI extraction failed: {e}")

# Method 2: Selector-based extraction
fields = pdf.get_form_fields()
for field in fields:
    print(f"{field.name}: {field.value}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your PDF example following the guide above
4. Test locally
5. Submit a pull request

## 📄 License

[Your license here]