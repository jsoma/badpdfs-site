---
slug: china-shi-san-wu-gui-hua-gang-yao-quan-wen
title: Extracting Tables from China's 5-Year Plan PDF
description: This PDF contains key data on China's 5-year plan. It's a research document
  with image-based tables, especially on page 8. It has Chinese text and requires
  OCR. Challenges include image/scan-based tables which complicate data extraction.
pdf: china-shi-san-wu-gui-hua-gang-yao-quan-wen.pdf
tags:
- image-based tables
- Chinese text
- research project
- OCR
- scanned document
file_size_mb: 5.02
page_count: 125
submitted_by: Yuqi Liao
language:
- Spanish
- Hindi
- Nepali
- Chinese
---
# Extracting Tables from China's 5-Year Plan PDF

This PDF contains key data on China's 5-year plan. It's a research document with image-based tables, especially on page 8. It has Chinese text and requires OCR. Challenges include image/scan-based tables which complicate data extraction.

```python
from natural_pdf import PDF

pdf = PDF("china-shi-san-wu-gui-hua-gang-yao-quan-wen.pdf")
pdf.show(cols=6)
```