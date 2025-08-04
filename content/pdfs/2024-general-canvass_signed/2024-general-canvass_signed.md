---
slug: 2024-general-canvass_signed
title: Extracting Precinct-Level Vote Counts from Elko County Presidential Race PDF
description: This PDF contains precinct-level unofficial vote counts for the 2024
  Presidential race in Elko County, NV. It has 125 pages and is vital for analyzing
  voting patterns in Hispanic-majority neighborhoods. Challenges include faint ink,
  inconsistent text orientation, and a poor scan quality, making OCR necessary for
  extraction.
pdf: 2024-general-canvass_signed.pdf
tags:
- Elko County
- 2024 Presidential Race
- Precinct-Level Data
- OCR Needed
- Poor Scan Quality
- Voting Patterns
file_size_mb: 37.27
page_count: 125
submitted_by: Paroma Soni
---
# Extracting Precinct-Level Vote Counts from Elko County Presidential Race PDF

This PDF contains precinct-level unofficial vote counts for the 2024 Presidential race in Elko County, NV. It has 125 pages and is vital for analyzing voting patterns in Hispanic-majority neighborhoods. Challenges include faint ink, inconsistent text orientation, and a poor scan quality, making OCR necessary for extraction.

```python
from natural_pdf import PDF

pdf = PDF("2024-general-canvass_signed.pdf")
pdf.show(cols=6)
```