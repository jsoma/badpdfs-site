---
slug: april-to-june-2021-singlecdr
title: Extracting Company Resolution Plans from Insolvent Company Reports
description: This PDF consists of quarterly reports from the Insolvency and Bankruptcy
  Board of India about insolvent companies. The goal is to extract tables covering
  company-wise resolution plans, including admitted claim amounts and liquidation
  values. Challenges include garbled text which makes standard extraction methods
  ineffective, requiring manual data compilation for accuracy.
pdf: april-to-june-2021-singlecdr.pdf
tags:
- table extraction
- garbled text
- insolvency reports
- manual data entry
file_size_mb: 0.12
page_count: 4
submitted_by: Jasmin Nihalani
---
# Extracting Company Resolution Plans from Insolvent Company Reports

This PDF consists of quarterly reports from the Insolvency and Bankruptcy Board of India about insolvent companies. The goal is to extract tables covering company-wise resolution plans, including admitted claim amounts and liquidation values. Challenges include garbled text which makes standard extraction methods ineffective, requiring manual data compilation for accuracy.

```python
from natural_pdf import PDF

pdf = PDF("april-to-june-2021-singlecdr.pdf")
pdf.show(cols=6)
```