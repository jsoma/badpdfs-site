---
slug: indictb1h_14
title: Extracting a Complex Economic Data Table from a Hebrew PDF
description: This PDF contains an economic statistics table from Israel. Challenges
  include missing ruling lines on the table and multiple levels of row names, with
  indentation used to convey parent/child relationships. It has data in Hebrew, requiring
  rearrangement from display order to logical order due to the right-to-left script.
  No handwritten text or OCR needed. Only one page.
pdf: indictb1h_14.pdf
tags:
- Hebrew language
- No ruling lines
- Hierarchical data
- Right-to-left script
- Table extraction
file_size_mb: 0.02
page_count: 1
submitted_by: Jeremy Merrill
language:
- Hebrew
- Hebrew
---
# Extracting a Complex Economic Data Table from a Hebrew PDF

This PDF contains an economic statistics table from Israel. Challenges include missing ruling lines on the table and multiple levels of row names, with indentation used to convey parent/child relationships. It has data in Hebrew, requiring rearrangement from display order to logical order due to the right-to-left script. No handwritten text or OCR needed. Only one page.

```python
from natural_pdf import PDF

pdf = PDF("indictb1h_14.pdf")
page = pdf.pages[0]
page.show()
```