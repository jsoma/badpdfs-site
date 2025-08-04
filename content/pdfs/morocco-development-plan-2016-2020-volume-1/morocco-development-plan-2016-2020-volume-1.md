---
slug: morocco-development-plan-2016-2020-volume-1
title: Extracting Information from Moroccan Policy Document
description: This PDF contains a policy document relevant to Moroccan industry regulations.
  The primary objective here is to extract a comprehensive table found on page 179.
  Challenges include dealing with the Arabic language and ensuring the table, written
  in Arabic, is accurately captured despite potential formatting issues.
pdf: morocco-development-plan-2016-2020-volume-1.pdf
tags:
- Arabic
- Table Extraction
- Moroccan Regulations
- Industry Policy
- PDF
file_size_mb: 1.35
page_count: 185
submitted_by: Yuqi Liao
language:
- Arabic
- Arabic
---
# Extracting Information from Moroccan Policy Document

This PDF contains a policy document relevant to Moroccan industry regulations. The primary objective here is to extract a comprehensive table found on page 179. Challenges include dealing with the Arabic language and ensuring the table, written in Arabic, is accurately captured despite potential formatting issues.

```python
from natural_pdf import PDF

pdf = PDF("morocco-development-plan-2016-2020-volume-1.pdf")
pdf.show(cols=6)
```