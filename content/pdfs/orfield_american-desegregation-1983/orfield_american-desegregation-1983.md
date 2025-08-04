---
slug: orfield_american-desegregation-1983
title: Extracting Historical School Segregation Data from a Scanned Report
description: This PDF contains data from Gary Orfield's 1983 report on public school
  desegregation in the United States from 1968 to 1980. It includes valuable historical
  tables, which present unique extraction challenges. Challenges include randomly
  oriented pages, blurry text, and tables on the same page facing different directions.
  OCR is needed.
pdf: orfield_american-desegregation-1983.pdf
tags:
- historical data
- school desegregation
- scanned PDF
- table extraction
- orientation challenges
file_size_mb: 5.33
page_count: 35
submitted_by: Sharon Lurye
---
# Extracting Historical School Segregation Data from a Scanned Report

This PDF contains data from Gary Orfield's 1983 report on public school desegregation in the United States from 1968 to 1980. It includes valuable historical tables, which present unique extraction challenges. Challenges include randomly oriented pages, blurry text, and tables on the same page facing different directions. OCR is needed.

```python
from natural_pdf import PDF

pdf = PDF("orfield_american-desegregation-1983.pdf")
pdf.show(cols=6)
```