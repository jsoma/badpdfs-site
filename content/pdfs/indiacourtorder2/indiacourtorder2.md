---
slug: indiacourtorder2
title: Extraction Challenges in Patanjali vs. Facebook PDF
description: This PDF is a legal document from the India e-Courts portal about a case
  against Facebook by Patanjali founder Swami Ramdev. It has 59 pages, with sections
  in both English and Hindi. Challenges include locating URLs on pages 23-27 and in
  email screenshots towards the end. Background info on pages 28-32 is unreadable.
  It has a mix of handwritten notes and bad scanning quality. OCR is needed.
pdf: indiacourtorder2.pdf
tags:
- Legal Document
- 'Mixed language: English and Hindi'
- Handwritten Text
- Illegible Scans
- OCR Required
- URLs Extraction
file_size_mb: 15.97
page_count: 59
submitted_by: Paroma Soni
language:
- English
- Spanish
- Portuguese
- German
- Arabic
- Amharic
- Hindi
- Tamil
- Hebrew
- Devanagari
---
# Extraction Challenges in Patanjali vs. Facebook PDF

This PDF is a legal document from the India e-Courts portal about a case against Facebook by Patanjali founder Swami Ramdev. It has 59 pages, with sections in both English and Hindi. Challenges include locating URLs on pages 23-27 and in email screenshots towards the end. Background info on pages 28-32 is unreadable. It has a mix of handwritten notes and bad scanning quality. OCR is needed.

```python
from natural_pdf import PDF

pdf = PDF("indiacourtorder2.pdf")
pdf.show(cols=6)
```