---
slug: egypt-minister-decision-19-of-2016
title: Extracting Policy Data from Egypt's Scanned PDF
description: This PDF contains information from Egypt about industry policies for
  a research project on international regulations. It has three pages and uses Arabic
  script. Challenges include poor scan quality and handwritten notes, making extraction
  tricky. OCR is needed to handle both typewritten and handwritten elements.
pdf: egypt-minister-decision-19-of-2016.pdf
tags:
- Egypt
- Arabic
- Policy Extraction
- Handwritten Notes
- OCR Needed
file_size_mb: 1.74
page_count: 3
submitted_by: Yuqi Liao
language:
- Arabic
- Arabic
---
# Extracting Policy Data from Egypt's Scanned PDF

This PDF contains information from Egypt about industry policies for a research project on international regulations. It has three pages and uses Arabic script. Challenges include poor scan quality and handwritten notes, making extraction tricky. OCR is needed to handle both typewritten and handwritten elements.

```python
from natural_pdf import PDF

pdf = PDF("egypt-minister-decision-19-of-2016.pdf")
pdf.show(cols=6)
```