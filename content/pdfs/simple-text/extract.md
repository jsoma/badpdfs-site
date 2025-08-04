---
slug: "simple-text-extraction"
title: "Simple Text Extraction"
description: "A minimal example for testing"
pdf: "practice.pdf"
---

# Basic Setup

```python
try:
    from natural_pdf import PDF
    pdf = PDF("practice.pdf")
    print(f"PDF has {len(pdf.pages)} pages")
except ImportError:
    print("natural_pdf not installed - using mock data")
    # Create a mock PDF object for testing
    class MockPDF:
        def __init__(self, path):
            self.path = path
            self.pages = [MockPage() for _ in range(5)]
    
    class MockPage:
        def show(self):
            print("[Mock] Showing PDF page")
        
        def extract_text(self):
            return "This is mock text from the PDF page for testing purposes."
    
    pdf = MockPDF("practice.pdf")
    print(f"PDF has {len(pdf.pages)} pages")
```

# Show Page

```python
page = pdf.pages[0]
page.show()
```

# Extract Text

```python
text = page.extract_text()
print(text[:100])  # First 100 chars
```