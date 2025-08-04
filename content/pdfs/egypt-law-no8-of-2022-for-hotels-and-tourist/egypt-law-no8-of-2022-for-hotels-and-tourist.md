---
slug: egypt-law-no8-of-2022-for-hotels-and-tourist
title: Arabic Text Extraction from Industry Policy PDF
description: This PDF contains industry policies from various countries for comparative
  research. Challenges include extracting Arabic text over 23 pages without the need
  for OCR.
pdf: egypt-law-no8-of-2022-for-hotels-and-tourist.pdf
tags:
- Arabic Language
- Policy Documents
- Text Extraction
file_size_mb: 0.16
page_count: 23
submitted_by: Yuqi Liao
language:
- Arabic
- Arabic
---
# Arabic Text Extraction from Industry Policy PDF

This PDF contains industry policies from various countries for comparative research. Challenges include extracting Arabic text over 23 pages without the need for OCR.

```python
from natural_pdf import PDF

pdf = PDF("egypt-law-no8-of-2022-for-hotels-and-tourist.pdf")
pdf.show(cols=6)
```