---
slug: slovenia-svn_slovenia-school_questionnaire_ms22
title: Slovenian Table Extraction from PISA PDF
description: This PDF is from the Slovenian education agency about PISA, a student
  assessment by the OECD. Challenges include extracting a table in Slovenian on page
  80, which has radio buttons that can disrupt extraction.
pdf: slovenia-svn_slovenia-school_questionnaire_ms22.pdf
tags:
- Slovenian
- table-extraction
- PISA
- PDF-challenges
- radio-buttons
- OECD
file_size_mb: 0.57
page_count: 85
submitted_by: Yuqi Liao
language:
- English
- Slovenian
---
# Slovenian Table Extraction from PISA PDF

This PDF is from the Slovenian education agency about PISA, a student assessment by the OECD. Challenges include extracting a table in Slovenian on page 80, which has radio buttons that can disrupt extraction.

```python
from natural_pdf import PDF

pdf = PDF("slovenia-svn_slovenia-school_questionnaire_ms22.pdf")
pdf.show(cols=6)
```