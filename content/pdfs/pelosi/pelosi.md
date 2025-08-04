---
slug: pelosi
title: 'Financial Disclosure Table Extraction: Nancy Pelosi'
description: This PDF is a financial disclosure document for Nancy Pelosi from the
  House Clerk's website. Challenges include tables with tricky formatting, irregular
  column patterns, and no guiding lines. It is English text without handwriting, and
  although the PDF itself is password protected (now removed), it makes pinpoint extraction
  tough with conventional tools.
pdf: pelosi.pdf
tags:
- Financial Disclosure
- Complex Table Extraction
- Password Protected
file_size_mb: 0.16
page_count: 12
submitted_by: Chris Conrad
---
# Financial Disclosure Table Extraction: Nancy Pelosi

This PDF is a financial disclosure document for Nancy Pelosi from the House Clerk's website. Challenges include tables with tricky formatting, irregular column patterns, and no guiding lines. It is English text without handwriting, and although the PDF itself is password protected (now removed), it makes pinpoint extraction tough with conventional tools.

```python
from natural_pdf import PDF

pdf = PDF("pelosi.pdf")
pdf.show(cols=6)
```