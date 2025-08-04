---
slug: nepal-national-fertilizer-policy-2058
title: Extracting Scanned Nepali Text from PDF
description: This PDF contains Nepali text from a poorly scanned document, part of
  a research project on industry policies across countries. It has very low-quality
  scanned text that requires OCR for extraction.
pdf: nepal-national-fertilizer-policy-2058.pdf
tags:
- Nepali Text
- Poor Scan
- OCR Needed
file_size_mb: 0.38
page_count: 4
submitted_by: Yuqi Liao
language: Nepali
---
# Extracting Scanned Nepali Text from PDF

This PDF contains Nepali text from a poorly scanned document, part of a research project on industry policies across countries. It has very low-quality scanned text that requires OCR for extraction.

```python
from natural_pdf import PDF

pdf = PDF("nepal-national-fertilizer-policy-2058.pdf")
pdf.show(cols=6)
```