---
slug: serbia-zakon-o-naknadama-za-koriscenje-javnih
title: Extracting Complex Data from Serbian Regulatory PDF
description: This PDF contains parts of Serbian policy documents, crucial for a research
  project analyzing industry policies across countries. The challenge lies in extracting
  a large table that spans pages (page 90 to 97) and a math formula on page 98, all
  in Serbian. Both elements lack clear boundaries between pages, complicating extraction.
pdf: serbia-zakon-o-naknadama-za-koriscenje-javnih.pdf
tags:
- Serbian
- Large Tables
- Math Formulas
- Regulatory Documents
file_size_mb: 1.89
page_count: 120
submitted_by: Yuqi Liao
language: Serbian
---
# Extracting Complex Data from Serbian Regulatory PDF

This PDF contains parts of Serbian policy documents, crucial for a research project analyzing industry policies across countries. The challenge lies in extracting a large table that spans pages (page 90 to 97) and a math formula on page 98, all in Serbian. Both elements lack clear boundaries between pages, complicating extraction.

```python
from natural_pdf import PDF

pdf = PDF("serbia-zakon-o-naknadama-za-koriscenje-javnih.pdf")
pdf.show(cols=6)
```