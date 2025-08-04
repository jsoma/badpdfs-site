---
slug: mgi_ren-ji-gong-cun-de-xin-ji-yuan_jian-ti-zhong
title: Extracting Key Charts from a Chinese PDF
description: This PDF is for a research project on China's automation industry. It
  covers various formats like charts and tables, all in Chinese. Challenges include
  a wide layout and the mix of charts and tables, especially on pages 4 and 16.
pdf: mgi_ren-ji-gong-cun-de-xin-ji-yuan_jian-ti-zhong.pdf
tags:
- Chinese text
- Mixed content
- Wide format
- Research project
file_size_mb: 2.57
page_count: 13
submitted_by: Yuqi Liao
language:
- Spanish
- Hindi
- Nepali
- Chinese
---
# Extracting Key Charts from a Chinese PDF

This PDF is for a research project on China's automation industry. It covers various formats like charts and tables, all in Chinese. Challenges include a wide layout and the mix of charts and tables, especially on pages 4 and 16.

```python
from natural_pdf import PDF

pdf = PDF("mgi_ren-ji-gong-cun-de-xin-ji-yuan_jian-ti-zhong.pdf")
pdf.show(cols=6)
```