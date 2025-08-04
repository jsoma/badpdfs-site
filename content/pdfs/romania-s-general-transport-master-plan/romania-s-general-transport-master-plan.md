---
slug: romania-s-general-transport-master-plan
title: Extraction from Romanian Policy Document PDF
description: This PDF is a scan of a document containing Romanian industry policy
  data across various countries. Challenges include very hard to read graphs, such
  as Figure 2.3 on page 27, and extensive tables like Table 5.7 on page 248. OCR is
  needed for extracting this dense information.
pdf: romania-s-general-transport-master-plan.pdf
tags:
- Romanian document
- poor scan quality
- OCR required
- complex tables
- graph extraction
file_size_mb: 5.97
page_count: 300
submitted_by: Yuqi Liao
language: Romanian
---
# Extraction from Romanian Policy Document PDF

This PDF is a scan of a document containing Romanian industry policy data across various countries. Challenges include very hard to read graphs, such as Figure 2.3 on page 27, and extensive tables like Table 5.7 on page 248. OCR is needed for extracting this dense information.

```python
from natural_pdf import PDF

pdf = PDF("romania-s-general-transport-master-plan.pdf")
pdf.show(cols=6)
```