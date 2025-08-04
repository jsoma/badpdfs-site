---
slug: anexo_edital_6604_1743480-table
title: Extracting Tiny Tables from a Brazilian Tender Document
description: This PDF is a tender document from Brazil's open procurement portal,
  written in Brazilian Portuguese. Challenges include low-resolution tables with the
  world's smallest font size. It has 14 pages and requires OCR.
pdf: anexo_edital_6604_1743480-table.pdf
tags:
- low-resolution
- tiny-font-size
- Brazilian Portuguese
- procurement
- OCR needed
file_size_mb: 4.41
page_count: 14
submitted_by: Kuang Keng Kuek Ser
language: Spanish
---
# Extracting Tiny Tables from a Brazilian Tender Document

This PDF is a tender document from Brazil's open procurement portal, written in Brazilian Portuguese. Challenges include low-resolution tables with the world's smallest font size. It has 14 pages and requires OCR.

```python
from natural_pdf import PDF

pdf = PDF("anexo_edital_6604_1743480-table.pdf")
pdf.show(cols=6)
```