---
slug: july-2023-n4-temp-logs
title: Extracting Temperature Logs from TDCJ Documentation
description: This PDF is a handwritten document log from the Texas Department of Criminal
  Justice, detailing external temperature readings recorded in prisons. It tracks
  dates, times, temperatures, humidity, or wind speed, along with the recorder's name.
  Challenges include inconsistent use of symbols like degrees and percentages, handwritten
  entries, and a poorly laid out form. OCR is needed to handle the handwriting across
  31 pages.
pdf: july-2023-n4-temp-logs.pdf
tags:
- handwritten
- temperature logs
- OCR needed
- inconsistent format
- prison records
file_size_mb: 1.94
page_count: 31
submitted_by: Christian McDonald
---
# Extracting Temperature Logs from TDCJ Documentation

This PDF is a handwritten document log from the Texas Department of Criminal Justice, detailing external temperature readings recorded in prisons. It tracks dates, times, temperatures, humidity, or wind speed, along with the recorder's name. Challenges include inconsistent use of symbols like degrees and percentages, handwritten entries, and a poorly laid out form. OCR is needed to handle the handwriting across 31 pages.

```python
from natural_pdf import PDF

pdf = PDF("july-2023-n4-temp-logs.pdf")
pdf.show(cols=6)
```