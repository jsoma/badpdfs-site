---
slug: bus_map
title: Bus Route Intervals Extraction PDF
description: This PDF is a single-page document showing bus route intervals from the
  Tokyo Metropolitan Bureau of Transportation. Challenges include unclear colour codes
  with no provided legends. The PDF is in both English and Japanese. OCR is needed
  to extract data accurately.
pdf: bus_map.pdf
tags:
- Bus Routes
- Color Codes
- English and Japanese
- OCR Required
file_size_mb: 10.17
page_count: 1
submitted_by: Isabella
language:
- English
- Spanish
- Japanese
- Nepali
- Japanese
---
# Bus Route Intervals Extraction PDF

This PDF is a single-page document showing bus route intervals from the Tokyo Metropolitan Bureau of Transportation. Challenges include unclear colour codes with no provided legends. The PDF is in both English and Japanese. OCR is needed to extract data accurately.

```python
from natural_pdf import PDF

pdf = PDF("bus_map.pdf")
page = pdf.pages[0]
page.show()
```