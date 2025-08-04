---
slug: catalogo_de_los_santos_de_espana
title: Extracting Text from a 16th-Century Spanish Book on Saints
description: This PDF is a book in Spanish from the 1500s with content about saints.
  Challenges include its age, and the text might be in an early form of Spanish. There's
  no handwritten text, but it has 106 pages, and it's unclear if OCR is needed.
pdf: catalogo_de_los_santos_de_espana.pdf
tags:
- Spanish
- Historical Document
- 16th Century
- OCR Uncertainty
file_size_mb: 13.86
page_count: 106
submitted_by: Carly Schulman
language: Spanish?
---
# Extracting Text from a 16th-Century Spanish Book on Saints

This PDF is a book in Spanish from the 1500s with content about saints. Challenges include its age, and the text might be in an early form of Spanish. There's no handwritten text, but it has 106 pages, and it's unclear if OCR is needed.

```python
from natural_pdf import PDF

pdf = PDF("catalogo_de_los_santos_de_espana.pdf")
pdf.show(cols=6)
```