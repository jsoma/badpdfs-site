---
slug: serbia-zakon-o-naknadama-za-koriscenje-javnih
title: Extracting Complex Data from Serbian Regulatory PDF
description: This PDF contains parts of Serbian policy documents, crucial for a research
  project analyzing industry policies across countries. The challenge lies in extracting
  a large table that spans pages (page 90 to 97) and a math formula on page 98, all
  in Serbian. Both elements lack clear boundaries between pages, complicating extraction.
pdf: serbia-zakon-o-naknadama-za-koriscenje-javnih.pdf
tags:
- Serbian
- Large Tables
- Math Formulas
- Regulatory Documents
- multiple tables
- spanning pages
file_size_mb: 1.89
page_count: 120
submitted_by: Yuqi Liao
language: Serbian
published: true
---
# Extracting Complex Data from Serbian Regulatory PDF

This PDF contains parts of Serbian policy documents, crucial for a research project analyzing industry policies across countries. The challenge lies in extracting a large table that spans pages (page 90 to 97) and a math formula on page 98, all in Serbian. Both elements lack clear boundaries between pages, complicating extraction.

```python
from natural_pdf import PDF
from natural_pdf.analyzers.guides import Guides

pdf = PDF("serbia-zakon-o-naknadama-za-koriscenje-javnih.pdf")
pdf.pages[:8].show(cols=4)
```

The submitter mentioned specific pages, but it's more fun to say "between the page with this and the page with that."

```python
first_page = pdf.find(text="Prilog 7.").page
last_page = pdf.find(text='VISINA NAKNADE ZA ZAGAĐENJE VODA').page
pages = pdf.pages[first_page.index:last_page.index+1]
pages.show(cols=4)
```

We want everything between Table 4 and 5.

```python
region = (
    pages
    .find(text="Tabela 4")
    .below(
        until="text:contains(Tabela 5)",
        include_endpoint=False,
        multipage=True
    )
)
region.show(cols=4)
```

We want everything broken up by category, which is labeled as "RAZRED" in the document. We'll just split it into sections with those serving as headers.

```python
sections = region.get_sections('text:contains(RAZRED)', include_boundaries='none')
    
sections.show(cols=4)
```

Some of them have headers and some of them don't, which can make extraction tough. Here's one that spans two pages and has headers.

```python
sections[7].show(cols=2)
```

Since it has headers, we can just use `.to_df()`.

```python
sections[7].extract_table().to_df()
```

This next one does *not* have headers.

```python
sections[5].show(cols=2)
```

We'll just manually specify them, probably the easiest route.

```python
df = sections[5].extract_table().to_df(header=False)
df.columns = ['Naziv proizvoda', 'Opis proizvoda', 'Jed. mere', 'Naknada u dinarima po jedinici mere']
df
```

How do we find the math formula? Find the page that has it, then just ask for the image.

```python
page = pdf.find(text="Obračun naknade za neposredno zagađenje voda").page
page.find("image").show()
```

If we were fancier we'd probably use [surya](https://github.com/datalab-to/surya) to convert it, but Natural PDF can't extract images like that just yet (I don't think?).