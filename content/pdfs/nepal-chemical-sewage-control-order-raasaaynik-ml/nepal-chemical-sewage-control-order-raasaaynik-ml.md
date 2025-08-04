---
slug: nepal-chemical-sewage-control-order-raasaaynik-ml
title: Navigating Nepali Table Extraction from a Legal PDF
description: The PDF is a document used in research focused on comparing industry
  policy across various countries, featuring laws and policy briefs from Nepal. Challenges
  include extracting a table located on page 30 amidst text, which is written in Nepali.
  No OCR is needed, but it is embedded within a non-trivial mix of elements. The document
  spans 33 pages.
pdf: nepal-chemical-sewage-control-order-raasaaynik-ml.pdf
tags:
- Nepali Text
- Table Extraction
- Legal Documents
file_size_mb: 0.3
page_count: 33
submitted_by: Yuqi Liao
language: Nepali
---
# Navigating Nepali Table Extraction from a Legal PDF

The PDF is a document used in research focused on comparing industry policy across various countries, featuring laws and policy briefs from Nepal. Challenges include extracting a table located on page 30 amidst text, which is written in Nepali. No OCR is needed, but it is embedded within a non-trivial mix of elements. The document spans 33 pages.

```python
from natural_pdf import PDF

pdf = PDF("nepal-chemical-sewage-control-order-raasaaynik-ml.pdf")
pdf.show(cols=6)
```