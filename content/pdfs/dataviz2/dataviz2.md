---
slug: dataviz2
title: Leslie Lohman Museum Digital Archive Poster
description: This PDF is a photo of a poster from a graduate student poster competition
  about the Leslie Lohman Museum's digital archive history. Challenges include excessive
  wordiness, poor font choices, and a cluttered design. It has no clear timeline or
  direct access methods to the collection. OCR is needed.
pdf: dataviz2.pdf
tags:
- poster extraction
- wordy text
- poor design
- digital archive
file_size_mb: 0.62
page_count: 1
submitted_by: V
---
# Leslie Lohman Museum Digital Archive Poster

This PDF is a photo of a poster from a graduate student poster competition about the Leslie Lohman Museum's digital archive history. Challenges include excessive wordiness, poor font choices, and a cluttered design. It has no clear timeline or direct access methods to the collection. OCR is needed.

```python
from natural_pdf import PDF

pdf = PDF("dataviz2.pdf")
page = pdf.pages[0]
page.show()
```