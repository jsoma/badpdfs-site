---
slug: reservation-of-wards-and-post-of-chairperson-of
title: Extracting Election Tables From Assam PDF
description: This PDF contains data from the local elections in Assam, India. It has
  two tables with crucial information. Challenges include skewed page scans that need
  correction. OCR is needed to pull text from the images. It's in English, so no language
  barrier.
pdf: reservation-of-wards-and-post-of-chairperson-of.pdf
tags:
- Assam Elections
- Skewed Scans
- Table Extraction
- OCR Needed
file_size_mb: 0.95
page_count: 8
submitted_by: Gaurav
---
# Extracting Election Tables From Assam PDF

This PDF contains data from the local elections in Assam, India. It has two tables with crucial information. Challenges include skewed page scans that need correction. OCR is needed to pull text from the images. It's in English, so no language barrier.

```python
from natural_pdf import PDF

pdf = PDF("reservation-of-wards-and-post-of-chairperson-of.pdf")
pdf.show(cols=6)
```