---
slug: min-guo-cong-shu-di-er-bian-02052-1-zhong-guo-yu
title: Extracting Table of Contents from Traditional Chinese Book
description: This PDF is a scanned book from the late Republic of China period focused
  on the Latinization of the Chinese language. Challenges include processing a poorly
  scanned document with Traditional Chinese text. OCR is needed to successfully extract
  the table of contents.
pdf: min-guo-cong-shu-di-er-bian-02052-1-zhong-guo-yu.pdf
tags:
- Traditional Chinese
- OCR
- Poor Scan Quality
- Latinization of Chinese Language
file_size_mb: 23.48
page_count: 584
submitted_by: Yuqi Liao
language:
- Spanish
- Hindi
- Nepali
- Chinese
---
# Extracting Table of Contents from Traditional Chinese Book

This PDF is a scanned book from the late Republic of China period focused on the Latinization of the Chinese language. Challenges include processing a poorly scanned document with Traditional Chinese text. OCR is needed to successfully extract the table of contents.

```python
from natural_pdf import PDF

pdf = PDF("min-guo-cong-shu-di-er-bian-02052-1-zhong-guo-yu.pdf")
pdf.show(cols=6)
```