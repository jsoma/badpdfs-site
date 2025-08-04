---
slug: serbia-state-budget-2022
title: Extracting Industry Policy Tables from Serbian PDF
description: This PDF contains various industry policy tables from Serbia starting
  at page 63. It has long and wide tables in Serbian, which are challenging to extract
  cleanly due to the language and format.
pdf: serbia-state-budget-2022.pdf
tags:
- Serbian
- large tables
- policy extraction
- wide tables
file_size_mb: 2.99
page_count: 252
submitted_by: Yuqi Liao
language: Serbian
---
# Extracting Industry Policy Tables from Serbian PDF

This PDF contains various industry policy tables from Serbia starting at page 63. It has long and wide tables in Serbian, which are challenging to extract cleanly due to the language and format.

```python
from natural_pdf import PDF

pdf = PDF("serbia-state-budget-2022.pdf")
pdf.show(cols=6)
```