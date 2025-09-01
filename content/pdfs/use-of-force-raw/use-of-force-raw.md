---
slug: use-of-force-raw
title: Extracting Use-of-Force Records from Vancouver Police PDF
description: This PDF contains detailed records of Vancouver Police's use-of-force incidents, provided after a public records request by journalists. Challenges include its very very very small font size and lots of empty whitespace.
pdf: use-of-force-raw.pdf
tags:
- small font
- public records
- tables
- sparse
file_size_mb: 0.7
page_count: 4
submitted_by: Brandon Roberts
language:
- English
published: true

---

# Extracting Use-of-Force Records from Vancouver Police PDF

This PDF contains detailed records of Vancouver Police's use-of-force incidents, provided after a public records request by journalists. Challenges include its very small font size and lots of empty whitespace.

```python
from natural_pdf import PDF

pdf = PDF("use-of-force-raw.pdf")
page = pdf.pages[0]
page.show()
```

Let's find all the headers, they're the text at the top of the pag, which means they have the smallest `y0`.

```python
headers = page.find_all('text[y0=min()]')
headers.extract_each_text()
```

We can now use those headers to create guides that fit between each column.

```python
from natural_pdf.analyzers.guides import Guides

guides = Guides(page)
guides.vertical.from_headers(headers)
guides.show()
```

Once we've established the columns, we're free to extract the table. [pdfplumber](https://github.com/jsvine/pdfplumber) is smart enough behind the scenes to know what each row is.

```python
guides.extract_table().to_df()
```

## Combining the results for every page

If you provide a list of pages, guides can extract the tables from each of them. It will also do nice things like automatically remove duplicate column headers without you even asking!

```python
df = guides.extract_table(pdf.pages).to_df()
print("You found", len(df), "rows")

df.tail()
```