---
slug: grad-plus-authorization_2024-25-002-
title: Pratt Institute's Inaccessible Loan Application PDF
description: This PDF is a student loan application form sent by Pratt to its students.
  Challenges include outdated web screenshot images that are blurry and don't match
  any known version of the site, causing confusion and accessibility issues. OCR is
  needed for clarity as the document is nearly unreadable.
pdf: grad-plus-authorization_2024-25-002-.pdf
tags:
- student loans
- inaccessible design
- PDF extraction
- OCR needed
file_size_mb: 0.11
page_count: 1
submitted_by: V
---
# Pratt Institute's Inaccessible Loan Application PDF

This PDF is a student loan application form sent by Pratt to its students. Challenges include outdated web screenshot images that are blurry and don't match any known version of the site, causing confusion and accessibility issues. OCR is needed for clarity as the document is nearly unreadable.

```python
from natural_pdf import PDF

pdf = PDF("grad-plus-authorization_2024-25-002-.pdf")
page = pdf.pages[0]
page.show()
```