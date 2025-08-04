---
slug: 1790_us_census_whole_number_of_persons
title: Census Data Extraction from 1790 U.S. Census PDF
description: This PDF contains the extracted results from the 1790 United States Census,
  detailing population figures across towns, counties, and states. Challenges include
  deciphering vertically-aligned and upside-down cursive handwriting, often found
  in column headers. It has curly brackets that complicate identifying data types
  and population counts, especially noted in areas like New Jersey. OCR is needed
  to handle the handwritten text effectively.
pdf: 1790_us_census_whole_number_of_persons.pdf
tags:
- Data Extraction
- OCR
- Historical Census
- Handwritten Text
- Vertical Text
file_size_mb: 20.06
page_count: 56
submitted_by: Veronica Penney
---
# Census Data Extraction from 1790 U.S. Census PDF

This PDF contains the extracted results from the 1790 United States Census, detailing population figures across towns, counties, and states. Challenges include deciphering vertically-aligned and upside-down cursive handwriting, often found in column headers. It has curly brackets that complicate identifying data types and population counts, especially noted in areas like New Jersey. OCR is needed to handle the handwritten text effectively.

```python
from natural_pdf import PDF

pdf = PDF("1790_us_census_whole_number_of_persons.pdf")
pdf.show(cols=6)
```