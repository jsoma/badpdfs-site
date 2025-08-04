---
slug: gpo-cdoc-118sdoc13
title: Handling Complex Senate Expenditure PDFs
description: 'This PDF contains detailed tables of Senate office expenditures found
  on the Senate''s website. Challenges include inconsistent formatting that makes
  parsing tough. It''s a massive file with 2979 pages and no handwritten text, though
  it''s notorious for making extraction attempts give up due to its complexity. '
pdf: gpo-cdoc-118sdoc13.pdf
tags:
- Legislative Data
- Data Extraction
- PDF Tables
- Inconsistencies
- Government Documents
file_size_mb: 11.2
page_count: 2979
submitted_by: Derek Willis
---
# Handling Complex Senate Expenditure PDFs

This PDF contains detailed tables of Senate office expenditures found on the Senate's website. Challenges include inconsistent formatting that makes parsing tough. It's a massive file with 2979 pages and no handwritten text, though it's notorious for making extraction attempts give up due to its complexity. 

```python
from natural_pdf import PDF

pdf = PDF("gpo-cdoc-118sdoc13.pdf")
pdf.show(cols=6)
```