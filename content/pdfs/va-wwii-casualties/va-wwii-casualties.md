---
slug: va-wwii-casualties
title: Extracting WWII Army Casualty Data from Virginia PDF
description: The PDF contains a list of Army service members from Virginia who were
  killed or missing during WWII. Challenges include poor contrast and faded type.
  OCR is needed. It has uneven rows and columns, lacks data labels after the first
  page, and has no dividing lines between columns and rows. There is no punctuation,
  making extraction tricky.
pdf: va-wwii-casualties.pdf
tags:
- OCR
- WWII
- military-casualties
- PDF-extraction
- data-cleaning
file_size_mb: 14.54
page_count: 36
submitted_by: Emilia Ruzicka
---
# Extracting WWII Army Casualty Data from Virginia PDF

The PDF contains a list of Army service members from Virginia who were killed or missing during WWII. Challenges include poor contrast and faded type. OCR is needed. It has uneven rows and columns, lacks data labels after the first page, and has no dividing lines between columns and rows. There is no punctuation, making extraction tricky.

```python
from natural_pdf import PDF

pdf = PDF("va-wwii-casualties.pdf")
pdf.show(cols=6)
```