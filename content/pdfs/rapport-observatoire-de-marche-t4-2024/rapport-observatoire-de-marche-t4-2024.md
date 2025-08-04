---
slug: rapport-observatoire-de-marche-t4-2024
title: Extracting Telecom Penetration Data from DRC's Regulatory Report
description: This PDF is a recent report from DRC's Postal and Telecommunications
  Regulatory Authority. It covers information crucial for internet and phone-line
  penetration rates across the DRC. Challenges include inconsistent formatting, where
  one column of a table is machine-readable and another features images. French numbering
  separates thousands with spaces and uses commas instead of periods. Some tables
  are oriented sideways, complicating extraction.
pdf: rapport-observatoire-de-marche-t4-2024.pdf
tags:
- DRC Telecom Report
- French Formatting
- Table Layout Issues
- PDF Extraction
- Telecom Data
file_size_mb: 6.54
page_count: 130
submitted_by: Bennett Hanson
language:
- English
- French
---
# Extracting Telecom Penetration Data from DRC's Regulatory Report

This PDF is a recent report from DRC's Postal and Telecommunications Regulatory Authority. It covers information crucial for internet and phone-line penetration rates across the DRC. Challenges include inconsistent formatting, where one column of a table is machine-readable and another features images. French numbering separates thousands with spaces and uses commas instead of periods. Some tables are oriented sideways, complicating extraction.

```python
from natural_pdf import PDF

pdf = PDF("rapport-observatoire-de-marche-t4-2024.pdf")
pdf.show(cols=6)
```