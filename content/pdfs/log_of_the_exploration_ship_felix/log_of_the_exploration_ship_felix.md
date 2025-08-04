---
slug: log_of_the_exploration_ship_felix
title: Extraction of Historical Ship Log from UK National Archives
description: This PDF contains a ship log discovered through deep web searches, likely
  from the UK National Archives. Challenges include super old and handwritten text.
  OCR is needed to pull any information. It's quite a task to extract anything useful
  from its 59 pages.
pdf: log_of_the_exploration_ship_felix.pdf
tags:
- handwritten
- ship log
- OCR
- historical document
- multi-page
file_size_mb: 25.27
page_count: 59
submitted_by: Carly Schulman
---
# Extraction of Historical Ship Log from UK National Archives

This PDF contains a ship log discovered through deep web searches, likely from the UK National Archives. Challenges include super old and handwritten text. OCR is needed to pull any information. It's quite a task to extract anything useful from its 59 pages.

```python
from natural_pdf import PDF

pdf = PDF("log_of_the_exploration_ship_felix.pdf")
pdf.show(cols=6)
```