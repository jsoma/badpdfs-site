---
slug: sp-sem-papel-documento-anexo
title: Healthcare Exam Waitlist Table Extraction from PDF
description: This PDF contains a table with waitlist information for public healthcare
  exams and procedures in Sao Paulo, Brazil. Challenges include the need for OCR and
  dealing with its intricate PDF structure designed to obfuscate easy content extraction.
pdf: sp-sem-papel-documento-anexo.pdf
tags:
- PDF extraction
- Healthcare data
- OCR
- Sao Paulo Health Department
- Public records
- Information Access Law
file_size_mb: 2.82
page_count: 13
submitted_by: Carol Moreno
language: Spanish
---
# Healthcare Exam Waitlist Table Extraction from PDF

This PDF contains a table with waitlist information for public healthcare exams and procedures in Sao Paulo, Brazil. Challenges include the need for OCR and dealing with its intricate PDF structure designed to obfuscate easy content extraction.

```python
from natural_pdf import PDF

pdf = PDF("sp-sem-papel-documento-anexo.pdf")
pdf.show(cols=6)
```