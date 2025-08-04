---
slug: pinochet-bio
title: Complex Extraction of Pinochet's Biography
description: This PDF is a scanned typewritten biography of Chilean dictator Augusto
  Pinochet from the National Security Archive. Challenges include Spanish words with
  accents, strikethroughs, censored paragraphs, handwritten notes, and characters
  that copy incorrectly. OCR is needed.
pdf: pinochet-bio.pdf
tags:
- OCR
- Scanned Document
- Handwritten Notes
- Typewritten Text
- Language Translation Issues
file_size_mb: 0.62
page_count: 2
submitted_by: Carla Mandiola
---
# Complex Extraction of Pinochet's Biography

This PDF is a scanned typewritten biography of Chilean dictator Augusto Pinochet from the National Security Archive. Challenges include Spanish words with accents, strikethroughs, censored paragraphs, handwritten notes, and characters that copy incorrectly. OCR is needed.

```python
from natural_pdf import PDF

pdf = PDF("pinochet-bio.pdf")
pdf.show(cols=6)
```