---
slug: ethiopia-federal-civil-servants-proclamation
title: Extracting Ethiopian Texts from a Two-Column Policy PDF
description: This PDF contains policy documents from Ethiopia necessary for a comparative
  research project on industry regulations across countries. It consists of 65 pages
  of text in Ethiopian, arranged in two columns. Challenges include the two-column
  layout, which may complicate the extraction process. Luckily, there are no handwritten
  texts and no need for OCR. However, navigating the document's structure could require
  careful handling of the columns.
pdf: ethiopia-federal-civil-servants-proclamation.pdf
tags:
- Ethiopia
- Two-Column Layout
- Policy Documents
- Non-Latin Script
- Text Extraction
file_size_mb: 0.67
page_count: 65
submitted_by: Yuqi Liao
language: Hindi
---
# Extracting Ethiopian Texts from a Two-Column Policy PDF

This PDF contains policy documents from Ethiopia necessary for a comparative research project on industry regulations across countries. It consists of 65 pages of text in Ethiopian, arranged in two columns. Challenges include the two-column layout, which may complicate the extraction process. Luckily, there are no handwritten texts and no need for OCR. However, navigating the document's structure could require careful handling of the columns.

```python
from natural_pdf import PDF

pdf = PDF("ethiopia-federal-civil-servants-proclamation.pdf")
pdf.show(cols=6)
```