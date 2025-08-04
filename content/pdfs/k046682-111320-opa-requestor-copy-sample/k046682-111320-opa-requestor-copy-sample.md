---
slug: k046682-111320-opa-requestor-copy-sample
title: Disciplinary Log Extraction from Snohomish County Sheriff's Office PDF
description: This PDF is a disciplinary log from the Snohomish County Sheriff's Office.
  It's tricky because the table lacks lines and text overlaps, disrupting the layout.
  Challenges include redactions that skew text positioning and inconsistent vertical
  alignment, complicating row separation. OCR isn't needed and there are no handwritten
  texts. The document is five pages long and in English.
pdf: k046682-111320-opa-requestor-copy-sample.pdf
tags:
- unruled tables
- overlapping text
- text redactions
- vertical layout inconsistencies
- PDF extraction
file_size_mb: 0.67
page_count: 5
submitted_by: Brandon Roberts
language:
- English
- English
---
# Disciplinary Log Extraction from Snohomish County Sheriff's Office PDF

This PDF is a disciplinary log from the Snohomish County Sheriff's Office. It's tricky because the table lacks lines and text overlaps, disrupting the layout. Challenges include redactions that skew text positioning and inconsistent vertical alignment, complicating row separation. OCR isn't needed and there are no handwritten texts. The document is five pages long and in English.

```python
from natural_pdf import PDF

pdf = PDF("k046682-111320-opa-requestor-copy-sample.pdf")
pdf.show(cols=6)
```