---
slug: liberty-county-boe
title: Bad OCR in a board of education annual financial report
description: This PDF is all sorts of information about the Board of Education in Liberty County, Georgia
pdf: liberty-county-boe.pdf
tags:
- financial report
- multi-page
- OCR
- page navigation
file_size_mb: 2.1
page_count: 72
submitted_by: Maggie Lee
---
# Bad OCR in a board of education annual financial report

So we have a reasonably long PDF (72 pages) that we want to grab a single page of information from. On top of everything else the text recognition (OCR) is bad. We'll need to redo that, so we'll start by reading the PDF in with `text_layer=False` to have it discard the incorrect text.

```python
from natural_pdf import PDF

pdf = PDF("liberty-county-boe/liberty-county-boe.pdf", text_layer=False)
pdf.pages.show(cols=6)
```

Now we need to apply *new* OCR to it.

We're impatient and only care about one specific page, and we know the page is somewhere near the front. To speed things up, we'll apply OCR to a subset of the pages.

```python
pdf.pages[5:20].apply_ocr()
```

Now we can look for the content we're interested in.

```python
pdf.find(text="FINANCIAL HIGHLIGHTS").show()
```

Granted if our OCR was off we might not be able to just grab what we're looking for, but luckily it's printed very nicely and we can almost guarantee the text comes through well.

We can preview to make sure the page looks right...

```python
pdf.find(text="FINANCIAL HIGHLIGHTS").page
page.show()
```

...and then pull out the text, save it to a file, whatever we want.

```python
text = page.extract_text()
print(text)

with open("content.txt") as fp:
    fp.write(text)
```

If we wanted to pass this over to someone else to double-check, we could even save the page itself as an image. We use `.render()` instead of `.show()` because it by default won't include highlights and annotations and that kind of stuff.

```python
page.render().save("output.png")
```