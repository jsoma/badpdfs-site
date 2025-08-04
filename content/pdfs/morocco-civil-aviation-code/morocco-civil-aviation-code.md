---
slug: morocco-civil-aviation-code
title: Extracting Handwritten Moroccan Policy Docs in Arabic
description: This PDF contains scanned pages of Moroccan policy documents for a research
  project comparing industry regulations. It has scanned and handwritten text, especially
  on page 80. Challenges include Arabic script, handwritten notes, and OCR reliance.
pdf: morocco-civil-aviation-code.pdf
tags:
- Arabic Script
- Handwritten Notes
- OCR Required
- Scanned Document
- Policy Documents
file_size_mb: 4.2
page_count: 113
submitted_by: Yuqi Liao
language:
- Arabic
- Arabic
---
# Extracting Handwritten Moroccan Policy Docs in Arabic

This PDF contains scanned pages of Moroccan policy documents for a research project comparing industry regulations. It has scanned and handwritten text, especially on page 80. Challenges include Arabic script, handwritten notes, and OCR reliance.

```python
from natural_pdf import PDF

pdf = PDF("morocco-civil-aviation-code.pdf")
pdf.show(cols=6)
```