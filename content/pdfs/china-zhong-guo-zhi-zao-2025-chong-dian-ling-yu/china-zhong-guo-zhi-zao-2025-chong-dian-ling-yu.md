---
slug: china-zhong-guo-zhi-zao-2025-chong-dian-ling-yu
title: Extracting Timeline Chart from China 2025 PDF
description: This PDF discusses China's 2025 research project. The tricky part is
  the unique and non-standard timeline chart on page 5. Challenges include interpreting
  Chinese text and complex layouts without needing OCR.
pdf: china-zhong-guo-zhi-zao-2025-chong-dian-ling-yu.pdf
tags:
- Chinese text
- non-standard charts
- complex layouts
- timeline chart
- research project
file_size_mb: 20.34
page_count: 191
submitted_by: Yuqi Liao
language:
- Spanish
- Hindi
- Nepali
- Chinese
---
# Extracting Timeline Chart from China 2025 PDF

This PDF discusses China's 2025 research project. The tricky part is the unique and non-standard timeline chart on page 5. Challenges include interpreting Chinese text and complex layouts without needing OCR.

```python
from natural_pdf import PDF

pdf = PDF("china-zhong-guo-zhi-zao-2025-chong-dian-ling-yu.pdf")
pdf.show(cols=6)
```