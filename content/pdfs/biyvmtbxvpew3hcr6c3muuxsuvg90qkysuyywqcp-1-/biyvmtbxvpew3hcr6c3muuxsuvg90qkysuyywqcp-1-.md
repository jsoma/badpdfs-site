---
slug: biyvmtbxvpew3hcr6c3muuxsuvg90qkysuyywqcp-1-
title: Extracting Text From Ceará Estate Constitution PDF
description: This PDF is the constitutional document from the state of Ceará, Brazil,
  written in Portuguese. Challenges include text split into two columns, the presence
  of footnotes, and identifying strike-through text that needs recognition and preservation
  in the extracted output.
pdf: biyvmtbxvpew3hcr6c3muuxsuvg90qkysuyywqcp-1-.pdf
tags:
- Ceará Constitution
- Portuguese Text
- Column Layout
- Footnotes
- Strikethrough Text
file_size_mb: 12.28
page_count: 196
submitted_by: Carolina
language: Spanish
---
# Extracting Text From Ceará Estate Constitution PDF

This PDF is the constitutional document from the state of Ceará, Brazil, written in Portuguese. Challenges include text split into two columns, the presence of footnotes, and identifying strike-through text that needs recognition and preservation in the extracted output.

```python
from natural_pdf import PDF

pdf = PDF("biyvmtbxvpew3hcr6c3muuxsuvg90qkysuyywqcp-1-.pdf")
pdf.show(cols=6)
```