---
slug: mednine
title: Arabic Election Results Table Extraction from Mednine PDF
description: This PDF has a data table showing election results from the Tunisian
  region of Mednine. Challenges include spanning header cells and rotated headers.
  It has Arabic script.
pdf: mednine.pdf
tags:
- Election Results
- Arabic Script
- Table Extraction
- Header Challenges
file_size_mb: 0.24
page_count: 4
submitted_by: Jeremy Merrill
language:
- Arabic
published: true
---
# Arabic Election Results Table Extraction from Mednine PDF

This PDF has a data table showing election results from the Tunisian region of Mednine. Challenges include spanning header cells and rotated headers. It has Arabic script.

Updated for testing caching system with cascading dependencies!

```python
from natural_pdf import PDF

pdf = PDF("mednine.pdf")
pdf.show(cols=3)
```

I spent far too long making sure Natural PDF supports right-to-left scripts like Arabic. While I can't read them to confirm, I'm vaguely confident that the text we're pulling from the PDF is accurate.

/// tab | Multi-page flows
## Building a flow

Since this PDF is all one big long table with not much else in the way, we can most likely just stack all of the pages on top of each other with a Flow.

```python
from natural_pdf.flows import Flow

flow = Flow(pdf.pages, arrangement='vertical')
flow.show(width=300)
```

Flows are ways of connecting separate pages or regions vertically or horizontally.

## Extracting the table

Since we're using a flow we can just rest easy on `.extract_table()`, which automatically combines the tables across the entire flow.

```python
df = flow.extract_table().to_df(header=None)
df
```
///

/// tab | Manually combining dataframes
If you'd rather not use a Flow, an alternative is going through each page. Instead of a `for` loop I like to use `.apply`, as it keeps things a bit shorter. You could also use a list comprehension!

```python
import pandas as pd
dataframes = pdf.pages.apply(
    lambda page: page.extract_table().to_df(header=None)
)
print("Found", len(dataframes), "tables")

# Combine
df = pd.concat(dataframes, ignore_index=True)
df
```

///

I'm a big fan of taking as much information as possible, then cleaning it up later. We *could* spend time wrangling the column headers on the first page, spacing out grids, etc etc etc, but instead *let's just grab the whole thing and sort it out later*.

## Cleaning up the data

Now it just becomes an exercise in data cleanup! This is something AI coding tools are excellent at, so feel free to lean hard on them.

```python
# Use row 2 as header
df.columns = df.iloc[3].fillna(df.iloc[2]).str.replace("\n", " ")

# Drop the first 3 rows
df = df.iloc[4:].reset_index(drop=True)

# Remove spaces from numbers and convert to int
numeric_cols = df.columns[0:4]
df[numeric_cols] = df[numeric_cols].replace(r"\s+", "", regex=True).astype(int)
df
```