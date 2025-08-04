---
slug: russia-price-setting-in-the-sphere-of-regulated
title: Extracting Russian Math Formulas from Policy Comparison PDF
description: This PDF is part of a research project analyzing industry policies from
  different countries. Our goal is to extract math formulas in Russian, specifically
  noted on page 181. Challenges include navigating non-Latin scripts and ensuring
  formula precision during extraction. There are 222 pages, but no handwritten text
  or need for OCR.
pdf: russia-price-setting-in-the-sphere-of-regulated.pdf
tags:
- Math Formulas
- Russian Language
- Policy Analysis
- Non-Latin Scripts
file_size_mb: 1.75
page_count: 222
submitted_by: Yuqi Liao
language: Russian
---
# Extracting Russian Math Formulas from Policy Comparison PDF

This PDF is part of a research project analyzing industry policies from different countries. Our goal is to extract math formulas in Russian, specifically noted on page 181. Challenges include navigating non-Latin scripts and ensuring formula precision during extraction. There are 222 pages, but no handwritten text or need for OCR.

```python
from natural_pdf import PDF

pdf = PDF("russia-price-setting-in-the-sphere-of-regulated.pdf")
pdf.show(cols=6)
```