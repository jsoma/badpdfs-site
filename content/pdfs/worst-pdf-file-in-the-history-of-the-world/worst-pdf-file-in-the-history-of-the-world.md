---
slug: worst-pdf-file-in-the-history-of-the-world
title: Ugandan Company Ownership Records Extraction
description: This PDF contains records of company ownership from the registrar of
  companies in Uganda. It has both typed and handwritten text, along with tables.
  Challenges include legible sections obstructed by stamps, badly written text, and
  the need to convert scanned images into usable text. OCR might be required to process
  handwritten content effectively.
pdf: worst-pdf-file-in-the-history-of-the-world.pdf
tags:
- handwriting
- OCR
- scanned images
- stamps
- typed text
file_size_mb: 0.26
page_count: 3
submitted_by: Blanshe Musinguzi
language:
- English
- Hebrew
---
# Ugandan Company Ownership Records Extraction

This PDF contains records of company ownership from the registrar of companies in Uganda. It has both typed and handwritten text, along with tables. Challenges include legible sections obstructed by stamps, badly written text, and the need to convert scanned images into usable text. OCR might be required to process handwritten content effectively.

```python
from natural_pdf import PDF

pdf = PDF("worst-pdf-file-in-the-history-of-the-world.pdf")
pdf.show(cols=6)
```