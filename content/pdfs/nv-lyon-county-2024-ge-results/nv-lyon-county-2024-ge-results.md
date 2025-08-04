---
slug: nv-lyon-county-2024-ge-results
title: Parsing Presidential Votes in Lyon County NV PDF
description: This PDF contains precinct-level voting data from Lyon County, Nevada
  after the 2024 election. Challenges include the PDF being scanned with pages rotated
  at random, leading to misplacement of numbers during OCR. It takes careful manual
  checking to ensure accuracy.
pdf: nv-lyon-county-2024-ge-results.pdf
tags:
- OCR
- scanned document
- election data
- precinct analysis
- misaligned data
file_size_mb: 23.38
page_count: 76
submitted_by: Paroma Soni
---
# Parsing Presidential Votes in Lyon County NV PDF

This PDF contains precinct-level voting data from Lyon County, Nevada after the 2024 election. Challenges include the PDF being scanned with pages rotated at random, leading to misplacement of numbers during OCR. It takes careful manual checking to ensure accuracy.

```python
from natural_pdf import PDF

pdf = PDF("nv-lyon-county-2024-ge-results.pdf")
pdf.show(cols=6)
```