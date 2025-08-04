---
slug: osha-inspection-2011-ups-death
title: Extraction of UPS Heat Incident Report Data
description: This PDF contains a detailed OSHA case file on a UPS employee's heat-induced
  death in 2011. Challenges include dense information spread over 121 pages. It has
  scans of photos, handwritten statements, completed forms, finding reports, emails,
  and inspector's notes. OCR is needed.
pdf: osha-inspection-2011-ups-death.pdf
tags:
- handwriting
- OCR
- non-uniform formats
- heat incident
- public records
file_size_mb: 109.62
page_count: 121
submitted_by: Adiel Kaplan
---
# Extraction of UPS Heat Incident Report Data

This PDF contains a detailed OSHA case file on a UPS employee's heat-induced death in 2011. Challenges include dense information spread over 121 pages. It has scans of photos, handwritten statements, completed forms, finding reports, emails, and inspector's notes. OCR is needed.

```python
from natural_pdf import PDF

pdf = PDF("osha-inspection-2011-ups-death.pdf")
pdf.show(cols=6)
```