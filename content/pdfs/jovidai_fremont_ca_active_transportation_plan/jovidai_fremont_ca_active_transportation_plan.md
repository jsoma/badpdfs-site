---
slug: jovidai_fremont_ca_active_transportation_plan
title: Extracting Survey Data from Fremont's Public Records PDF
description: This PDF contains official records from the City of Fremont, focusing
  on responses to the Active Transportation Plan survey. Challenges include a small
  font size that makes the data hard to read and less clear for extraction. It has
  tables that don't translate well into spreadsheets, requiring OCR for better clarity.
pdf: jovidai_fremont_ca_active_transportation_plan.pdf
tags:
- PDF extraction
- public records
- active transportation
- small font size
- table formatting
- OCR required
file_size_mb: 1.06
page_count: 12
submitted_by: Jovi Dai
---
# Extracting Survey Data from Fremont's Public Records PDF

This PDF contains official records from the City of Fremont, focusing on responses to the Active Transportation Plan survey. Challenges include a small font size that makes the data hard to read and less clear for extraction. It has tables that don't translate well into spreadsheets, requiring OCR for better clarity.

```python
from natural_pdf import PDF

pdf = PDF("jovidai_fremont_ca_active_transportation_plan.pdf")
pdf.show(cols=6)
```