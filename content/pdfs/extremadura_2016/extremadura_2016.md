---
slug: extremadura_2016
title: Extracting Budget Tables from Spanish PDF
description: This PDF holds the 2016 budget for Extremadura, a region in Southwest
  Spain. Challenges include protection settings preventing page extraction. It has
  tables that appear as images, making extraction tricky. OCR is needed.
pdf: extremadura_2016.pdf
tags:
- OCR
- tables as images
- Spanish document
- protected PDF
- large document
file_size_mb: 23.08
page_count: 757
submitted_by: Olaya Argüeso Pérez
language:  Spanish
---
# Extracting Budget Tables from Spanish PDF

This PDF holds the 2016 budget for Extremadura, a region in Southwest Spain. Challenges include protection settings preventing page extraction. It has tables that appear as images, making extraction tricky. OCR is needed.

```python
from natural_pdf import PDF

pdf = PDF("extremadura_2016.pdf")
pdf.show(cols=6)
print('hello')
```
