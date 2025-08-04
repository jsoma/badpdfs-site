---
slug: nara_book1_sample
title: UFO Sightings and Investigations Extraction from 1949
description: This PDF is a collection of table entries documenting UFO sightings from
  1949, as part of the Project BLUE BOOK files. Challenges include needing OCR due
  to the old typeface and poor scan quality. It has inline handwriting, annotations,
  and redactions that complicate extraction. The format is hard to preserve with typical
  tools, making it tricky to convert into a clean table.
pdf: nara_book1_sample.pdf
tags:
- UFO sightings
- handwriting
- OCR needed
- historical documents
- scan quality
file_size_mb: 15.48
page_count: 11
submitted_by: Brandon Roberts
language:
- English
- English
---
# UFO Sightings and Investigations Extraction from 1949

This PDF is a collection of table entries documenting UFO sightings from 1949, as part of the Project BLUE BOOK files. Challenges include needing OCR due to the old typeface and poor scan quality. It has inline handwriting, annotations, and redactions that complicate extraction. The format is hard to preserve with typical tools, making it tricky to convert into a clean table.

```python
from natural_pdf import PDF

pdf = PDF("nara_book1_sample.pdf")
pdf.show(cols=6)
```