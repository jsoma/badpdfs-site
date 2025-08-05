---
slug: "basics"
title: "Natural PDF basics with text and tables"
description: "Learn the fundamentals of Natural PDF - opening PDFs, extracting text with layout preservation, selecting elements by criteria, spatial navigation, and managing exclusion zones. Perfect starting point for PDF data extraction."
pdf: "basics.pdf"
tags:
- Text Extraction
- Basic Usage
- Element Selection
- Spatial Navigation
- Tables
- Exclusion Zones
file_size_mb: 0.2
page_count: 1
submitted_by: Natural PDF Team
published: true
---

# Opening a PDF

Let's start by opening a PDF. Natural PDF can work with local files or URLs.

```python
from natural_pdf import PDF

pdf = PDF("basics.pdf")
page = pdf.pages[0]
page.show()
```

# Grabbing Page Text

You can extract text while preserving the layout, which maintains the spatial arrangement of text on the page.

```python
text = page.extract_text(layout=True)
print(text)
```

# Selecting Elements and Text

Natural PDF provides powerful selectors to find specific elements on the page.

## Select text in a rectangle

```python
text = page.find('rect').extract_text()
print(text)
```

## Find all text elements

```python
texts = page.find_all('text').extract_each_text()
for t in texts[:5]:  # Show first 5
    print(t)
```

## Find colored text

```python
# Find red text
red_text = page.find('text[color~=red]')
print(red_text.extract_text())
```

## Find text by content

```python
# Find text starting with specific string
text = page.find('text:contains("INS-")')
print(text.extract_text())
```

# Spatial Navigation

Natural PDF excels at spatial relationships between elements.

## Extract text to the right of a label

```python
# Extract text to the right of "Date:"
date_text = page.find(text="Date:").right(height='element').extract_text()
print(f"Date: {date_text}")
```

## Extract tables

```python
table = page.extract_table()
if table:
    df = table.to_df()
    print(df.head())
```

# Exclusion Zones

Sometimes you need to exclude headers, footers, or other unwanted areas from extraction.

## Exclude specific regions

```python
# Exclude top header area
top = page.region(top=0, left=0, height=80)
page.add_exclusion(top)

# Exclude area below last line
bottom = page.find_all("line")[-1].below()
page.add_exclusion(bottom)

# Now extract text without excluded areas
text = page.extract_text()
print(text)
```

## PDF-level exclusions

Apply exclusions to all pages in a PDF:

```python
# Add header exclusion to all pages
pdf.add_exclusion(lambda page: page.region(top=0, left=0, height=80))
```