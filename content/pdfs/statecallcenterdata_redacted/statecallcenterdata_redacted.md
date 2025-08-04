---
slug: statecallcenterdata_redacted
title: Extracting State Agency Call Center Wait Times from FOIA PDF
description: This PDF contains data on wait times at a state agency call center. The
  main focus is on the data on the first two pages, which matches other states' submission
  formats. The later pages provide granular breakdowns over several years. Challenges
  include it being heavily pixelated, making it hard to read numbers and text, with
  inconsistent and unreadable charts.
pdf: statecallcenterdata_redacted.pdf
tags:
- Call Center Data
- Pixelated Scan
- OCR Required
- Granular Breakdown
file_size_mb: 6.19
page_count: 66
submitted_by: Adiel Kaplan
published: true
---
# Extracting State Agency Call Center Wait Times from FOIA PDF

This PDF contains data on wait times at a state agency call center. The main focus is on the data on the first two pages, which matches other states' submission formats. The later pages provide granular breakdowns over several years. Challenges include it being heavily pixelated, making it hard to read numbers and text, with inconsistent and unreadable charts.

The submission said "the first two pages" so I'm going with that. The rest of the pages are *insane* and will need a wholly separate writeup.

```python
from natural_pdf import PDF

pdf = PDF("statecallcenterdata_redacted.pdf")
page = pdf.pages[0]
page.show()
```

The pages are images so they don't have text, but we can always double-check.

```python
# No results? Needs OCR!
print(page.extract_text())
```

I love [surya](https://github.com/datalab-to/surya) so I'm going to use it instead of the default of easyocr. Two ways to check the results: look at where it found text and look at what the text is.

```python
page.apply_ocr('surya')
page.find_all('text').show()
```

And now we'll look at what the text is.

```python
print(page.extract_text(layout=True))
```

To get the table area, we get everything from the "Figure" header down to "Please use the comments field"

```python
table_area = (
    page
    .find('text:contains(Figure)')
    .below(
        until='text:contains(Please use the comments)',
        include_endpoint=False
    )
)
table_area.show(crop='wide')
```

We need to cut it in on the sides a little bit, and expand it on the bottom. I just pick some manual values because I'm lazy, should probably be a better way to resize things based on selectors.

```python
table_area = (
    page
    .find('text:contains(Figure)')
    .below(
        until='text:contains(Please use the comments)',
        include_endpoint=False
    )
    .expand(
        right=-(page.width * 0.58),
        left=-30,
        bottom=3
    )
)
table_area.show(crop='wide')
```

Now we can see all the text in our area.

```python
table_area.find_all('text').show()
```

For some reason we can't just use `.extract_table('stream')` on this, even though there are some nice gaps between each column. Oh well!

Instead we'll throw three vertical dividers in and then shuffle then around until they don't intersect any of the text. The horizontal borders are easier because they're just lines.

```python
from natural_pdf.analyzers.guides import Guides

guide = Guides(table_area)
guide.vertical.divide(3)
guide.vertical.snap_to_whitespace(detection_method='text')
guide.horizontal.from_lines()
guide.show()
```

And now we can grab the table!

```python
df = (
  guide
  .extract_table()
  .to_df(
    header=['value', 'amount', 'comments']
  )
)
```

The next page is....... too hard for now.

```python
pdf.pages[1].show()
```