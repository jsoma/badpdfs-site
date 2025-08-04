---
slug: 1867_polish
title: Extracting Text from Old Polish 'Pierogi' Documents
description: This PDF contains a collection of old Polish documents with searches
  related to 'pierogi'. Challenges include weird or old formatting, Polish language,
  and uncertainty about whether OCR is needed. It has 37 pages with no handwritten
  text.
pdf: 1867_polish.pdf
tags:
- PDF extraction
- Old documents
- Polish language
- Text formatting challenges
file_size_mb: 2.93
page_count: 37
submitted_by: Carly Schulman
language: Polish
---
# Extracting Text from Old Polish 'Pierogi' Documents

This PDF contains a collection of old Polish documents with searches related to 'pierogi'. Challenges include weird or old formatting, Polish language, and uncertainty about whether OCR is needed. It has 37 pages with no handwritten text.

```python
from natural_pdf import PDF

pdf = PDF("1867_polish.pdf")
pdf.show(cols=6)
```