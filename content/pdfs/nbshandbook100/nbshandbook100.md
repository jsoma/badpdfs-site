---
slug: nbshandbook100
title: Extracting Data and Insights from Copper Wire Handbook
description: This PDF is a 52-page handbook from the 1966 National Bureau of Standards.
  It's about the correct usage of copper wire in electrical work. Challenges include
  wonky data tables, inconsistent font sizes, and formulas. Some pages are sideways.
  There are also a few hand-drawn shapes scattered throughout.
pdf: nbshandbook100.pdf
tags:
- CopperWire
- DataTables
- Formulas
- InconsistentFonts
- SidewaysPages
file_size_mb: 4.55
page_count: 52
submitted_by: Jared Canty
---
# Extracting Data and Insights from Copper Wire Handbook

This PDF is a 52-page handbook from the 1966 National Bureau of Standards. It's about the correct usage of copper wire in electrical work. Challenges include wonky data tables, inconsistent font sizes, and formulas. Some pages are sideways. There are also a few hand-drawn shapes scattered throughout.

```python
from natural_pdf import PDF

pdf = PDF("nbshandbook100.pdf")
pdf.show(cols=6)
```