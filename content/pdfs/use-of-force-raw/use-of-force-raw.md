---
slug: use-of-force-raw
title: Extracting Use-of-Force Records from Vancouver Police PDF
description: This PDF contains detailed records of Vancouver Police's use-of-force
  incidents, provided after a public records request by journalists. Challenges include
  its very small font size, making manual reading difficult, although extraction tools
  handle it quite well.
pdf: use-of-force-raw.pdf
tags:
- PDF extraction
- use of force records
- small font
- Vancouver Police
- public records
file_size_mb: 0.7
page_count: 4
submitted_by: Brandon Roberts
language:
- English
- English
---
# Extracting Use-of-Force Records from Vancouver Police PDF

This PDF contains detailed records of Vancouver Police's use-of-force incidents, provided after a public records request by journalists. Challenges include its very small font size, making manual reading difficult, although extraction tools handle it quite well.

```python
from natural_pdf import PDF

pdf = PDF("use-of-force-raw.pdf")
pdf.show(cols=6)
```