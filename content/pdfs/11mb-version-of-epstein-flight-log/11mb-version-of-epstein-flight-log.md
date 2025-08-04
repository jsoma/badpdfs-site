---
slug: 11mb-version-of-epstein-flight-log
title: Extracting Flight Log Entries from Epstein-Related PDF
description: This PDF contains the original flight logs from the U.S vs. Maxwell case.
  The goal is extracting the flight log entries into a table format. Challenges include
  poor handwriting, requiring OCR for text recognition, and complex document edits
  reducing clarity.
pdf: 11mb-version-of-epstein-flight-log.pdf
tags:
- flight_logs
- handwriting
- OCR
- complex_edits
- PDF_extraction
file_size_mb: 11.09
page_count: 118
submitted_by: Sanjin Ibrahimovic
---
# Extracting Flight Log Entries from Epstein-Related PDF

This PDF contains the original flight logs from the U.S vs. Maxwell case. The goal is extracting the flight log entries into a table format. Challenges include poor handwriting, requiring OCR for text recognition, and complex document edits reducing clarity.

```python
from natural_pdf import PDF

pdf = PDF("11mb-version-of-epstein-flight-log.pdf")
pdf.show(cols=6)
```