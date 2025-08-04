---
slug: francia-politica_de_privacidad_vfinal_fr_230321
title: Extracting French Privacy Policy from Desigual's PDF
description: This PDF contains the privacy policy of Desigual's online store. It has
  perfectly readable text when opened in a viewer. Challenges include its content
  transformed into vectors. Language is French. OCR is needed across 3 pages.
pdf: francia-politica_de_privacidad_vfinal_fr_230321.pdf
tags:
- OCR
- Privacy Policy
- Vector Text
- French
file_size_mb: 0.97
page_count: 3
submitted_by: Matti Schneider
language:
- English
- French
---
# Extracting French Privacy Policy from Desigual's PDF

This PDF contains the privacy policy of Desigual's online store. It has perfectly readable text when opened in a viewer. Challenges include its content transformed into vectors. Language is French. OCR is needed across 3 pages.

```python
from natural_pdf import PDF

pdf = PDF("francia-politica_de_privacidad_vfinal_fr_230321.pdf")
pdf.show(cols=6)
```