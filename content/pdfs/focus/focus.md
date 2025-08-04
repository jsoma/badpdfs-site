---
slug: focus
title: Extracting Economic Data from Brazil's Central Bank PDF
description: This PDF is the weekly “Focus” report from Brazil’s central bank with
  economic projections and statistics. Challenges include commas instead of decimal
  points, images showing projection changes, and tables without border lines that
  merge during extraction.
pdf: focus.pdf
tags:
- Brazil
- Economic Data
- PDF Extraction
- Tables without Borders
- Comma as Decimal
- Image Interpretation
file_size_mb: 0.87
page_count: 2
submitted_by: Giovanna serafim
language: Spanish
published: true
---
# Extracting Economic Data from Brazil's Central Bank PDF

This PDF is the weekly “Focus” report from Brazil’s central bank with economic projections and statistics. Challenges include commas instead of decimal points, images showing projection changes, and tables without border lines that merge during extraction.

```python
from natural_pdf import PDF

pdf = PDF("focus.pdf")
page = pdf.pages[0]
page.show()
```

Let's cut out the part of the page we're interested in: everything from **Expectativas** to the long, light text that starts with **comportamento**.

```python
data = (
    page
    .find(text='Expectativas')
    .below(
        until='text:contains(comportamento)',
        include_endpoint=False
    )
)
    
data.show(crop=True)
```

## Grabbing headers

While we could type out the column names on the left, it's probably easier to just scrape them from the page. We start from IPCA, move down, clip it to the section we cut out earlier (otherwise it runs down the whole page), then find all of the text that even somewhat overlaps.

```python
row_names = (
    data
    .find(text='IPCA')
    .below(width='element', include_source=True)
    .clip(data)
    .find_all('text', overlap='partial')
)
headers = row_names.extract_each_text()
headers
```

/// tab | Using sections
## Horizontal sections

While you usually use `.get_sections` to split pages vertically, you can also do it horizontally. In this case we'll find the year headers - four numbers in a row, size 10 font - and use them as our breakpoints.

```python
sections = (
    data.get_sections(
        start_elements="text[size~=10]:regex(\d\d\d\d)",
        include_boundaries='start',
        orientation='horizontal'
    )
)
sections.show()
```

We'll take the first table as an example. We don't want all of that junk up top – it's easy to retype multi-row headers – so we'll dial it back in a bit.

```python
(
    sections[0]
    .expand(top=-50)
    .show()
)
```

Then we'll ask it to extract the content using the **stream** method, which uses the space between text. Even though we can see lines and backgrounds and all sorts of things, stream works consistently when other approaches don't!

```python
(
    sections[0]
    .expand(top=-50, right=0)
    .extract_table('stream')
    .to_df(header=False)
    .dropna(axis=0, how='all')
)
```

We include the `.dropna` in there because stream injects some phantom rows full of empty values.

## Looping through sections

Now that we know how it works from one section, let's do it for all of them. We'll use `.apply` so that it creates a list of dataframes that we can combine later on.

```python
dataframes = sections.apply(lambda section: (
    section
        .expand(top=-50, right=0)
        .extract_table('stream')
        .to_df(header=False)
        .dropna(axis=0, how='all')
        .assign(
            year=section.find('text[size~=10]:regex(\d\d\d\d)').extract_text(),
            value=headers
        )
    )
)

import pandas as pd

pd.concat(dataframes, ignore_index=True)
```


import pandas as pd

pd.concat(dataframes, ignore_index=True)
///

/// tab | Manually selecting tables

## Grabbing tables

We start by grabbing the space between the 2025 and 2026 headers.

```python
(
    data
    .find('text:contains(2025)')
    .right(
        until='text:contains(2026)',
        include_source=True,
        include_endpoint=False
    )
).show()
```

...then we move down...

```python
(
    data
    .find('text:contains(2025)')
    .right(
        until='text:contains(2026)',
        include_source=True,
        include_endpoint=False
    )
    .below(width='element')
).show()
```

...then we nudge the top down a little bit and clip it to the size of the region of interest (the `data` region).

```python
table = (
    data
    .find('text:contains(2025)')
    .right(
        until='text:contains(2026)',
        include_source=True,
        include_endpoint=False
    )
    .below(width='element')
    .expand(top=-20)
    .clip(data)
)

table.show()
```

We could try to figure out something magic with all of the headers and colors and backgrounds and blah blah blah, but it's easier to just extract the table using the "stream" method, which looks at the gaps between rows and columns. While there *are* actual boundaries between the rows, I promise stream works the best.

```python
df_2025 = table.expand(top=-5).extract_table('stream').to_df(header=False)
df_2025
```

It needs a *little* cleanup. Due to using the steam approach we got some extra (empty) columns, but we can just drop them with pandas. We'll also insert the year and the row titles that we grabbed up above. 

```python
df_2025 = df_2025.dropna(axis=0, how='all')
df_2025.insert(0, 'year', 2025)
df_2025.insert(0, 'value', headers)
df_2025
```

### Working on all the other tables

2026 is basically the same.

```python
table = (
    data
    .find('text:contains(2026)')
    .right(
        until='text:contains(2027)',
        include_source=True,
        include_endpoint=False
    )
    .below(width='element')
    .expand(top=-20)
    .clip(data)
)
table.show()
```

```python
df_2026 = table.expand(top=-5).extract_table('stream').to_df(header=False).dropna(axis=0, how='all')
df_2026.insert(0, 'year', 2026)
df_2026.insert(0, 'value', headers)
df_2026
```

As is 2027.

```python
table = (
    data
    .find('text:contains(2027)')
    .right(
        until='text:contains(2028)',
        include_source=True,
        include_endpoint=False
    )
    .below(width='element')
    .expand(top=-20)
    .clip(data)
)
df_2027 = table.expand(top=-5).extract_table('stream').to_df(header=False).dropna(axis=0, how='all')
df_2027.insert(0, 'year', 2027)
df_2027.insert(0, 'value', headers)
df_2027
```

2028 is a *little* different because it doesn't including an endpoint on the right. We just blast on through until we hit the right-hand side of the page.

```python
table = (
    data
    .find('text:contains(2028)')
    .right(include_source=True)
    .below(width='element')
    .expand(top=-20)
    .clip(data)
)
df_2028 = table.expand(top=-5).extract_table('stream').to_df(header=False).dropna(axis=0, how='all')
df_2028.insert(0, 'year', 2028)
df_2028.insert(0, 'value', headers)
df_2028
```

Now we'll set up the dataframes in a nice long list to combine in the next step.

```python
dataframes = [df_2025, df_2026, df_2027, df_2028]
```

///

## Combining our data

Now that we have a list of dataframes (no matter which path we took) we can just use pandas to concatenate them.

```python
import pandas as pd

df = pd.concat(dataframes, ignore_index=True)
df
```

There we go!