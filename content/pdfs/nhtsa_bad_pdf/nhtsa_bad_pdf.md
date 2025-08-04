---
slug: nhtsa_bad_pdf
title: Structuring Data from NHTSA Incident Report PDFs
description: This PDF contains a NHTSA incident report under the Special General Order
  for cars with ADAS systems, released under FOIA. Challenges include it's a scan
  with checkboxes formed in a car shape and requires OCR for proper extraction.
pdf: nhtsa_bad_pdf.pdf
tags:
- NHTSA
- incident report
- scanned PDF
- check box
- ADAS
- FOIA
- OCR needed
file_size_mb: 0.88
page_count: 2
submitted_by: Jeremy Merrill
---
# Structuring Data from NHTSA Incident Report PDFs

This PDF contains a NHTSA incident report under the Special General Order for cars with ADAS systems, released under FOIA. Challenges include it's a scan with checkboxes formed in a car shape and requires OCR for proper extraction.

```python
from natural_pdf import PDF

pdf = PDF("nhtsa_bad_pdf.pdf")
pdf.show(cols=6)
```