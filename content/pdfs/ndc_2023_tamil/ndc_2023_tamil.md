---
slug: ndc_2023_tamil
title: Extracting Renewable Energy Tables from Sri Lankan NDC Scheme PDF (2021-2030)
description: This PDF discusses the 'Implementation of Nationally Determined Contributions
  Scheme (2021-2030)' for Sri Lanka. Challenges include complex tables with many variables,
  formatted in a way that's tricky for scraping. OCR is needed as the document uses
  Tamil, a non-Latin script. 257 pages in total.
pdf: ndc_2023_tamil.pdf
tags:
- Complex Tables
- Tamil Language
- OCR Required
- Renewable Energy
- Non-Latin Script
file_size_mb: 2.49
page_count: 257
submitted_by: Bennett Hanson
language:
- Amharic
- Tamil
---
# Extracting Renewable Energy Tables from Sri Lankan NDC Scheme PDF (2021-2030)

This PDF discusses the 'Implementation of Nationally Determined Contributions Scheme (2021-2030)' for Sri Lanka. Challenges include complex tables with many variables, formatted in a way that's tricky for scraping. OCR is needed as the document uses Tamil, a non-Latin script. 257 pages in total.

```python
from natural_pdf import PDF

pdf = PDF("ndc_2023_tamil.pdf")
pdf.show(cols=6)
```