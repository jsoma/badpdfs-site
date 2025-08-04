---
slug: china-2016nian-zhong-guo-ben-ke-sheng-jiu-ye-bao
title: Extracting Graph and Table Data from a Comprehensive Research PDF
description: This PDF is from a research project on career choices for Chinese undergraduates.
  It has numerous graphs and tables scattered throughout. Challenges include extracting
  specific data from pages 180 and 181, amidst many other similar elements. The text
  is in Chinese, though no OCR is required as it doesn't contain handwritten text.
pdf: china-2016nian-zhong-guo-ben-ke-sheng-jiu-ye-bao.pdf
tags:
- PDF extraction
- Chinese script
- tables and graphs
file_size_mb: 4.9
page_count: 200
submitted_by: Yuqi Liao
language:
- Spanish
- Hindi
- Nepali
- Chinese
---
# Extracting Graph and Table Data from a Comprehensive Research PDF

This PDF is from a research project on career choices for Chinese undergraduates. It has numerous graphs and tables scattered throughout. Challenges include extracting specific data from pages 180 and 181, amidst many other similar elements. The text is in Chinese, though no OCR is required as it doesn't contain handwritten text.

```python
from natural_pdf import PDF

pdf = PDF("china-2016nian-zhong-guo-ben-ke-sheng-jiu-ye-bao.pdf")
pdf.show(cols=6)
```