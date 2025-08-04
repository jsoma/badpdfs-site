---
slug: 8218224_vicente-gonzalez
title: Extracting Financial Investments from House of Representatives Filings
description: This PDF contains 67 pages of investment filings from the House of Representatives.
  It has lots of handwritten notes from one representative. Everyone else typed their
  documents. Nothing is OCR'd. Challenges include bad handwriting and the need for
  OCR to make it readable.
pdf: 8218224_vicente-gonzalez.pdf
tags:
- handwriting
- financial_investments
- OCR_needed
- government_filings
file_size_mb: 2.55
page_count: 67
submitted_by: Madison Hall
---
# Extracting Financial Investments from House of Representatives Filings

This PDF contains 67 pages of investment filings from the House of Representatives. It has lots of handwritten notes from one representative. Everyone else typed their documents. Nothing is OCR'd. Challenges include bad handwriting and the need for OCR to make it readable.

```python
from natural_pdf import PDF

pdf = PDF("8218224_vicente-gonzalez.pdf")
pdf.show(cols=6)
```