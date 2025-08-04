---
slug: "natural-pdf-basics-with-text-and-tables"
title: "Natural PDF basics with text and tables"
description: "Workshop example: Natural PDF basics with text and tables"
pdf: "practice.pdf"
tags: ["workshop"]
---

# Installing Natural PDF

There are a LOT of possible extras (a lot of them AI-flavored) inside of Natural PDF, but we'll start by just installing the basics. You use `"natural_pdf[all]"` if you want *everything*.

```bash
pip install --upgrade --quiet "natural-pdf @ git+https://github.com/jsoma/natural-pdf.git"
```

# Opening a PDF

**We'll start by opening a PDF.**

You can use a PDF on your own computer, or you can use one from a URL. I'll start by using one from a URL to make everything a bit easier.

```python
from natural_pdf import PDF

pdf = PDF("practice.pdf")
pdf
```

You can find the pages of the pdf under `pdf.pages`, let's grab the first one.

```python
page = pdf.pages[0]
page
```

Pretty boring so far, eh? Let's take a look at the page itself.

```python
page.show()
```

Incredible!!! Congratulations, you've opened your first PDF with Natural PDF.

# Grabbing page text

Most of the time when we're working with PDFs you're interested in the text on the page.

```python
# text = page.extract_text()
text = page.extract_text(layout=True)
# text
print(text)
```

`layout=True` is a useful addition if you want to see a text-only representation of the page, and sometimes it helps with data extraction.

# Selecting elements and grabbing specific text

You rarely want all of the text, though. How would you describe the **INS-UP70N51NCL41R** text?

- It's in a box
- It's the second text on a page
- It's red
- It starts with "INS"

## Selecting objects: "It's in the box"

```python
# page.find('rect')
# page.find('rect').show()
page.find('rect').show(crop=True)
```

```python
text = page.find('rect').extract_text()
print(text)
```

### Selecting multiple objects: "It's the second piece of text"

```python
page.find_all('text').show()
```

```python
texts = page.find_all('text').extract_each_text()

texts[:5]
```

```python
texts[1]
```

### Finding by attributes: "It's the red text"

```python
red_text = page.find('text[color~=red]')
red_text.show(crop=True)
```

```python
red_text.extract_text()
```

## Searching by text: "It starts with INS-"

```python
text = page.find('text:contains("INS-")')
# text = page.find('text:starts-with("INS-")')
text.show(crop=True)
```

```python
text.extract_text()
```

What about "Chicago, Ill."? It's grey, so...

```python
page.find("text[color~=grey]")
```

Amazing!!! If we want some more details about what *kind* of grey it is, we can inspect all of the text.

## Rough locations: It's in the top right

```python
corner = page.region(bottom=100, left=page.width-300)
corner.show(crop=True)
corner.extract_text()
```

# Learning about the page

How do we know what's on the page? `page.describe()` can help!

```python
page.describe()
```

```python
page.find_all('text').inspect()
```

```python
page.find_all('text[size<10][font_family=Helvetica]').show()
```

## Spatial navigation

What else is on the page that we can extract? How about the **date?** We want to find **Date:** and grab everything to the right of it.

```python
# page.find(text="Date").show()
page.find(text="Date").right(height='element').extract_text()
```

And the **site?** We want to grab 'site', then keep going right until we see a piece of text.

```python
site = (
    page
    .find(text="Site")
    .right(height='element',
           until='text')
    .expand(right=-10)
)
# site.show(crop=True)
site.extract_text()
```

How about **Violation Count?**

```python
page.find(text="Violation Count").right(height='element').extract_text()
```

The **Summary** is a little bit more difficult. How would you describe where it is?

```python
page.find(text="Summary").right(height='element').extract_text()
```

```python
summary = (
    page
    .find(text="Summary")
    .below(include_source=True, until='line')
)
summary.show()
summary.extract_text()
```

## Grabbing tables

Everyone loves extracting tables from PDFs! You can do that here: just do `page.extract_table()`. Easy!!!

```python
table = page.extract_table()
table.to_df()
```

What about a page with **multiple tables?**

In most PDF processing libraries you just say, "give me all of the tables!" and then figure out which one you want. In Natural PDF, the _proper_ way to do it is find the area you know the table is in and extract it alone. 

```python
page.find('text[size>10]:bold:contains("Violations")').below(
    until='text:contains(Jungle Health)',
    include_endpoint=False
).show(crop=True)
```

```python
(
    page
    .find('text[size>10]:bold:contains("Violations")')
    .below(
        until='text:contains(Jungle Health)',
        include_endpoint=False
    )
    .extract_table()
    .to_df()
)
```

# Ignoring text with exclusion zones

What if we have like two hundred of these forms, and they all look the same, and all we want is the top, text-y part?

Instead of writing code about what we *want*, we can also write code about what we *don't want*. These are called [**exclusion zones**](https://jsoma.github.io/natural-pdf/tutorials/05-excluding-content/).

```python
from natural_pdf import PDF

pdf = PDF("practice.pdf")
page = pdf.pages[0]
```

```python
page.show()
```

```python
text = page.extract_text()
print(text)
```

```python
top = page.region(top=0, left=0, height=80)
bottom = page.find_all("line")[-1].below()

top.highlight(existing='replace')
bottom.highlight()
page.show()
```

```python
page.clear_highlights()

page.add_exclusion(top)
page.add_exclusion(bottom)

page.show(exclusions='red')
```

```python
text = page.extract_text()
print(text)
```

Any time there is recurring text - headers, footers, even *stamps on the page you want to ignore*, you can just add them as an exclusion. 

It's also possible to add exclusions across *multiple pages*. In the example below, every time you load a new page up it applies the PDF-level exclusion on it. Write it once, be done with it forever!

```python
pdf.add_exclusion(lambda page: page.region(top=0, left=0, height=80))
pdf.add_exclusion(lambda page: page.find_all("line")[-1].below())
```

## Next steps

What about **when the text isn't so easy to access?** Time to move on to our next notebook!
