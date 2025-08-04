---
slug: obgyn-professional-development-newsletter-volume
title: DEI Newsletter OCR Extraction Challenge
description: This PDF is a newsletter from the DEI office in the Ob/Gyn Department
  at Columbia, created using Canva in 2021. Challenges include the use of all caps
  and wide spacing, which make it difficult for text recognition to determine word
  boundaries. OCR might be needed if text appears jumbled.
pdf: obgyn-professional-development-newsletter-volume.pdf
tags:
- DEI Newsletter
- Text Recognition
- OCR Challenge
- PDF Extraction
file_size_mb: 4.98
page_count: 2
submitted_by: Felicite Fallon
---
# DEI Newsletter OCR Extraction Challenge

This PDF is a newsletter from the DEI office in the Ob/Gyn Department at Columbia, created using Canva in 2021. Challenges include the use of all caps and wide spacing, which make it difficult for text recognition to determine word boundaries. OCR might be needed if text appears jumbled.

```python
from natural_pdf import PDF

pdf = PDF("obgyn-professional-development-newsletter-volume.pdf")
pdf.show(cols=6)
```