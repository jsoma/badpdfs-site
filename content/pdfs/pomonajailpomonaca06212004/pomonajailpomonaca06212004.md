---
slug: pomonajailpomonaca06212004
title: ICE Detention Facilities Compliance Report Extraction
description: This PDF is an ICE report on compliance among detention facilities over
  the last 20-30 years. Our aim is to extract facility statuses and contract signatories'
  names and dates. Challenges include strange redactions, blobby text, poor contrast,
  and ineffective OCR. It has handwritten signatures and dates that are redacted.
pdf: pomonajailpomonaca06212004.pdf
tags:
- ICE compliance report
- Redacted text
- Handwriting
- OCR needed
- Text extraction issues
- Columns
file_size_mb: 41.36
page_count: 26
submitted_by: Paroma Soni
published: true
---
# ICE Detention Facilities Compliance Report Extraction

This PDF is an ICE report on compliance among detention facilities over the last 20-30 years. Our aim is to extract facility statuses and contract signatories' names and dates. Challenges include strange redactions, blobby text, poor contrast, and ineffective OCR. It has handwritten signatures and dates that are redacted.

Let's take a look at one of the form pages. **The text recognition isn't very good** so wer'e going to load it in with `text_layer=False` and do our own OCR.

```python
from natural_pdf import PDF

pdf = PDF("pomonajailpomonaca06212004.pdf", text_layer=False)
page = pdf.pages[3]
page.show()
```

Looks like it's going to be a nightmare! Let's apply OCR to convert the images to text.

```python
# pdf.apply_ocr(resolution=192) if we wanted the whole thing
page.apply_ocr(resolution=192)
text = page.extract_text()[:200]
print(text)
```

### Selecting content in a column

We need to grab the content on column at a time, so let's start by focusing on the left column.

```python
left_col = page.region(right=page.width/2 - 15)
left_col.show()
```

We could also pull one specific section of the page if we wanted to

```python
with left_col.within() as col:
    portion = (
        left_col
        .find("text:closest(Name and Location)")
        .below(
          until='text:contains(ICE Information)',
          include_endpoint=False
        )
    )
portion.show(crop=True)
```

### Fuzzy matching

Because there might be errors in reading the text, we're going to use `text:closest` to find our labels instead of `text:contains`. The code below will find the text that's *closest* to "Dates of Review," even though it will actually come through as `Date[s] of Review` (I wasn't sure whether it would understand the brackets or convert them to parens).

```python
label = (
    left_col
    .find("text:closest(Dates of Review)")
)
print("Found", label.extract_text())
label.show(crop=20)
```

Now we want to find the **first piece of text under it**. Normally we'd just be able to say "find me the text below this," but sometimes when you run OCR on a page the content overlaps. By using `anchor='start'` we tell Natural PDF that "below" counts as anything below the *top* of the source text.

```python
with left_col.within() as col:
    answer = (
      label
      .below(until='text', anchor='start')
    )
    print(answer.extract_text('words'))
```

Notice that we use `left_col.within()` to make sure it doesnt' grab any text outside of the box. We also use `.endpoint` to make sure we're talking about only the text Natural PDF found directly below the label.

We can duplicate this pattern for anything with the same top/bottom pattern. For example, the **county**.

```python
(
  left_col
  .find("text:closest(County)")
  .show(crop=50)
)
```

It just takes the same code:

```python
with left_col.within() as col:
    label = left_col.find("text:closest(County)")
    answer = label.below(until='text')
    print(answer.extract_text('words'))
```

This is an alternative approach to the `.endpoint` method we saw before. Sometimes text below the answer overlaps slightly with the answer, and if Natural PDF pulls character-by-character it pollutes the answer. By asking for complete "words" it should pull the right stuff.

### Checkboxes

This part is the hard one. We'll find the section under **Previous Rating**, expand it a bit (OCR never lines up perfectly) and trim out the whitespace to make it a nice tight box.

```python
with left_col.within() as col:
    label = left_col.find("text:closest(Previous Rating)")
    answer = label.below(until='text')
checkbox_region = answer.expand(5).trim()
checkbox_region.show(crop=True)
```

In an ideal world I'd have trained a nice custom checkbox analyzer, but *I did and it didn't work*. So instead we're going to train our own with a few examples. We'll start by grabbing the three checkboxes here.

```python
def get_checkbox(region):
  return region.left(20).expand(top=3)

region1 = get_checkbox(checkbox_region.find(text='Acceptable'))
region2 = get_checkbox(checkbox_region.find(text='Deficient'))
region3 = get_checkbox(checkbox_region.find(text='At-Risk'))
(region1 + region2 + region3).show(crop=True)
```

Now we'll add the first one as an example of a **checked** box and the second as an example of an **unchecked** box.

```python
from natural_pdf import Judge

judge = Judge("checkboxes", labels=["checked", "unchecked"])
judge.forget(delete=True)

judge.add(region1, "checked")
judge.add(region2, "unchecked")
```

What's it think of the third one?

```python
judge.decide(region3)
```

Now let's add a bunch more!

```python
judge.add(get_checkbox(page.find(text='Field Office')))
judge.add(get_checkbox(page.find(text='HQ Review')))
judge.add(get_checkbox(page.find('text[text=Court Order]')))
judge.add(get_checkbox(page.find('text[text=Major Litigation]')))
judge.add(get_checkbox(page.find('text[text=Class Action Order]')))
judge.add(get_checkbox(page.find('text[text=No]')))
```

What does it think about them, only knowing two examples?

```python
judge.inspect()
```

Usually you'd take a couple forms worth of checkboxes and mark them all, then send your judge on to the rest of your forms. You can do a quick graphical scoring interface with `judge.teach()`. Sadly I can't show it to you here because it's interacive.

```python
# judge.teach()
```

But I promise once you do it you can easily see whether a checkbox on your document is checked or not.