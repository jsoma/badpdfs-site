---
slug: cpi_haryana
title: CPI Financial Statement from Election Commission of India
description: This PDF is a financial document listing the CPI party's resources and
  expenses. Challenges include handwritten numerical values, scattered details, and
  lack of OCR support. Extraction requires careful attention due to these handwritten
  entries and distributed information across 22 pages.
pdf: cpi_haryana.pdf
tags:
- handwritten
- election commission
- english
- financial data
- complex extraction
file_size_mb: 3.74
page_count: 22
submitted_by: Jasmin Nihalani
---
# CPI Financial Statement from Election Commission of India

This PDF is a financial document listing the CPI party's resources and expenses. Challenges include handwritten numerical values, scattered details, and lack of OCR support. Extraction requires careful attention due to these handwritten entries and distributed information across 22 pages.

```python
from natural_pdf import PDF

pdf = PDF("cpi_haryana.pdf")
pdf.show(cols=6)
```