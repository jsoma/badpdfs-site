---
slug: doc-06-approved-expenses-07012022-06302023
title: Arizona Education Savings Account Purchase Records PDF
description: This PDF contains detailed records of purchases made by parents through
  Arizona's Education Savings Account. Challenges include dissecting over 24,000 pages
  of data, which display columns for vendor, categories, and item descriptions. It
  has a layout that merges fields, complicating clean extractions.
pdf: doc-06-approved-expenses-07012022-06302023.pdf
tags:
- Data Extraction
- PDF Parsing
- Public Records
- Educational Purchases
- Large Documents
file_size_mb: 62.89
page_count: 24909
submitted_by: Sharon Lurye
---
# Arizona Education Savings Account Purchase Records PDF

This PDF contains detailed records of purchases made by parents through Arizona's Education Savings Account. Challenges include dissecting over 24,000 pages of data, which display columns for vendor, categories, and item descriptions. It has a layout that merges fields, complicating clean extractions.

```python
from natural_pdf import PDF

pdf = PDF("doc-06-approved-expenses-07012022-06302023.pdf")
pdf.show(cols=6)
```