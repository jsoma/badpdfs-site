---
slug: statecallcenterdata_redacted
title: Extracting State Agency Call Center Wait Times from FOIA PDF
description: This PDF contains data on wait times at a state agency call center. The
  main focus is on the data on the first two pages, which matches other states' submission
  formats. The later pages provide granular breakdowns over several years. Challenges
  include it being heavily pixelated, making it hard to read numbers and text, with
  inconsistent and unreadable charts.
pdf: statecallcenterdata_redacted.pdf
tags:
- Call Center Data
- Pixelated Scan
- OCR Required
- Granular Breakdown
file_size_mb: 6.19
page_count: 66
submitted_by: Adiel Kaplan
---
# Extracting State Agency Call Center Wait Times from FOIA PDF

This PDF contains data on wait times at a state agency call center. The main focus is on the data on the first two pages, which matches other states' submission formats. The later pages provide granular breakdowns over several years. Challenges include it being heavily pixelated, making it hard to read numbers and text, with inconsistent and unreadable charts.

```python
from natural_pdf import PDF

pdf = PDF("statecallcenterdata_redacted.pdf")
pdf.show(cols=6)
```