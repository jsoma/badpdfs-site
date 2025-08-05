---
slug: "page-structure"
title: "Working with page structure"
description: "Extract text from complex multi-column layouts while maintaining proper reading order. Learn techniques for handling academic papers, newsletters, and documents with intricate column structures using Natural PDF's layout detection features."
pdf: "multicolumn.pdf"
tags:
- Multi-Column Layout
- Reading Order
- Text Flow
- Academic Papers
- Layout Detection
- Table Extraction
- YOLO
- TATR
file_size_mb: 0.8
page_count: 1
submitted_by: Natural PDF Team
published: true
---

# Multi-page flows

*Sometimes* you have data that flows over multiple columns, or pages, or just... isn't arranged in a "normal" top-to-bottom way.

```python
from natural_pdf import PDF

pdf = PDF("multicolumn.pdf")
page = pdf.pages[0]
page.show()
```

Natural PDF deals with these through [reflowing pages](https://jsoma.github.io/natural-pdf/reflowing-pages/), where you grab specific regions of a page and then paste them back together either vertically or horizontally.

In this example we're splitting the page into three columns.

```python
left = page.region(left=0, right=page.width/3, top=0, bottom=page.height)
mid = page.region(left=page.width/3, right=page.width/3*2, top=0, bottom=page.height)
right = page.region(left=page.width/3*2, right=page.width, top=0, bottom=page.height)
page.highlight(left, mid, right)
```

Now let's **stack them on top of each other**.

```python
from natural_pdf.flows import Flow

stacked = [left, mid, right]
flow = Flow(segments=stacked, arrangement="vertical")
```

Now any time we want to use spatial comparisons, like "find something below this," it *just works*.

```python
region = (
    flow
    .find('text:contains("Table one")')
    .below(
        until='text:contains("Table two")',
        include_endpoint=False
    )
)
region.show()
```

It works for text, it works for tables, it works for **anything**. Let's see how we can get both tables on the page.

First we find the bold headers – we need to say `width > 10` because otherwise it pulls some weird tiny empty boxes.

```python
(
    flow
    .find_all('text[width>10]:bold')
    .show()
)
```

Then we take each of those headers, and go down down down until we either hit another bold header *or* the "Here is a bit more text" text. 

```python
regions = (
    flow
    .find_all('text[width>10]:bold')
    .below(
        until='text[width>10]:bold|text:contains("Here is a bit")',
        include_endpoint=False
    )
)
regions.show()

```

Now we can use `.extract_table()` on *each individual region* to give us however many tables.

```python
regions[0].extract_table().to_df()
```

```python
# Combine them if we want
import pandas as pd

dfs = regions.apply(lambda region: region.extract_table().to_df())
merged = pd.concat(dfs, ignore_index=True)
```

# Layout analysis and magic table extraction

Similar to how we have feelings about what things are on a page - headers, tables, graphics – computers also have opinions! Just like some AI models have been trained to do things like identify pictures of cats and dogs or spell check, others are capable of **layout analysis** - [YOLO](https://huggingface.co/spaces/omoured/YOLOv11-Document-Layout-Analysis), [surya](https://github.com/datalab-to/surya), etc etc etc. There are a million! [TATR](https://github.com/microsoft/table-transformer) is one of the useful ones for us, it's *just for table detection*.

But honestly: they're mostly trained on academic papers, so they aren't very good at the kinds of awful documents that journalists have to deal with. And with Natural PDF, you're probably selecting `text[size>12]:bold` in order to find headlines, anyway. *But* if your page has no readable text, they might be able to provide some useful information.

Let's start with [YOLO](https://github.com/opendatalab/DocLayout-YOLO), the default.

```python
from natural_pdf import PDF

pdf = PDF("needs-ocr.pdf")
page = pdf.pages[0]
```

```python
# default is YOLO
page.analyze_layout()
page.find_all('region').show(group_by='type')
```

```python
page.find('table').apply_ocr()
text = page.extract_text()
print(text)
```

### Better layout analysis with tables

Let's see what **TATR** - Microsoft's table transformer – finds for us.

```python
page.analyze_layout('tatr')
page.find_all('region').show(group_by='type')
```

There's just *so much stuff* that TATR is finding that it's all overlapping.

For example, we can just look at one piece at a time.

```python
# table-cell
# table-row
# table-column
page.find_all('region[type=table-column]').show(crop=True)
```

```python
# Grab all of the columns
cols = page.find_all('region[type=table-column]')

# Take one of the columns and apply OCR to it
cols[2].apply_ocr()
text = cols[2].extract_text()
print(text)
```

```python
len(cols[2].find_all('text[source=ocr]'))
```

```python
page.find('table').show()
```

```python
data = page.find('table').extract_table()
data
```

## Why YOLO?

I think YOLO is pretty good for isolating a part of a page that has a table, then using Guides to break it down.

```python
page.analyze_layout()
page.find_all('region').show(group_by="type")
```

```python
table_area = page.find("region[type=table]")
table_area.apply_ocr()
```

```python
text = table_area.extract_text()
print(text)
```

```python
from natural_pdf.analyzers import Guides

guides = Guides(table_area)
guides.vertical.from_lines(threshold=0.6)
guides.horizontal.from_lines(threshold=0.6)
guides.show()
```

```python
guides.extract_table().to_df()
```
