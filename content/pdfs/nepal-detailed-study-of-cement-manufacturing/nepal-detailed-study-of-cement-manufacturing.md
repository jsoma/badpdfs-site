---
slug: nepal-detailed-study-of-cement-manufacturing
title: PDF Table Extraction from Nepal's Policy Document
description: This PDF is part of a research project comparing international industry
  policies. It contains Nepal's industry regulations and spans 121 pages. Challenges
  include extracting a long table (Annex 6) from pages 89 to 92 without any need for
  OCR.
pdf: nepal-detailed-study-of-cement-manufacturing.pdf
tags:
- Long Table Extraction
- Policy Comparison
- International Regulations
file_size_mb: 4.24
page_count: 121
submitted_by: Yuqi Liao
---
# PDF Table Extraction from Nepal's Policy Document

This PDF is part of a research project comparing international industry policies. It contains Nepal's industry regulations and spans 121 pages. Challenges include extracting a long table (Annex 6) from pages 89 to 92 without any need for OCR.

```python
from natural_pdf import PDF

pdf = PDF("nepal-detailed-study-of-cement-manufacturing.pdf")
pdf.show(cols=6)
```