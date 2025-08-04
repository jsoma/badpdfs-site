---
slug: pomonajailpomonaca06212004
title: ICE Detention Facilities Compliance Report Extraction
description: This PDF is an ICE report on compliance among detention facilities over
  the last 20-30 years. Our aim is to extract facility statuses and contract signatories'
  names and dates. Challenges include strange redactions, blobby text, poor contrast,
  and ineffective OCR. It has handwritten signatures and dates that are redacted.
pdf: pomonajailpomonaca06212004.pdf
tags:
- ICE compliance report
- Redacted text
- Handwriting
- OCR needed
- Text extraction issues
file_size_mb: 41.36
page_count: 26
submitted_by: Paroma Soni
---
# ICE Detention Facilities Compliance Report Extraction

This PDF is an ICE report on compliance among detention facilities over the last 20-30 years. Our aim is to extract facility statuses and contract signatories' names and dates. Challenges include strange redactions, blobby text, poor contrast, and ineffective OCR. It has handwritten signatures and dates that are redacted.

```python
from natural_pdf import PDF

pdf = PDF("pomonajailpomonaca06212004.pdf")
pdf.show(cols=6)
```