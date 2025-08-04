---
slug: "text-extraction-basics"
title: "Text Extraction Basics"
description: "Learn fundamental PDF text extraction techniques using Natural PDF - from simple text grabbing to spatial navigation and table extraction"
pdf: "practice.pdf"
tags: ["text-extraction", "tables", "spatial-navigation", "selectors"]
---

# Opening a PDF

We'll start by opening a PDF inspection form and exploring various ways to extract its content.

```python
from natural_pdf import PDF

pdf = PDF("practice.pdf")
page = pdf.pages[0]
page.show()
```

# Grabbing Page Text

Most of the time when working with PDFs, you're interested in the text on the page. The `layout=True` option preserves the visual structure.

```python
text = page.extract_text(layout=True)
print(text)
```

# Selecting Elements and Grabbing Specific Text

You rarely want all of the text. Let's extract the inspection ID number **INS-UP70N51NCL41R** using different selection strategies.

## Method 1: "It's in a box"

```python
# Find the rectangle and extract its content
rect_text = page.find('rect').extract_text()
print(rect_text)
```

```python
# Visualize what we found
page.find('rect').show(crop=True)
```

## Method 2: "It's the second piece of text"

```python
# Get all text elements
texts = page.find_all('text').extract_each_text()
print(f"Second text element: {texts[1]}")
```

## Method 3: "It's red text"

```python
# Find text by color attribute
red_text = page.find('text[color~=red]')
red_text.show(crop=True)
print(red_text.extract_text())
```

## Method 4: "It starts with INS-"

```python
# Search by text content
ins_text = page.find('text:contains("INS-")')
ins_text.show(crop=True)
print(ins_text.extract_text())
```

# Learning About the Page

Use `describe()` to understand what elements are available on the page.

```python
page.describe()
```

You can also inspect specific elements to see their attributes:

```python
# Find all small Helvetica text
page.find_all('text[size<10][font_family=Helvetica]').show()
```

# Spatial Navigation

Natural PDF excels at extracting data based on spatial relationships. Let's extract form fields by finding labels and navigating from them.

## Extract the Date

```python
# Find "Date:" and get text to its right
date = page.find(text="Date").right(height='element').extract_text()
print(f"Date: {date}")
```

## Extract the Site

```python
# Navigate right until we hit text
site = (
    page
    .find(text="Site")
    .right(height='element', until='text')
    .expand(right=-10)  # Trim extra space
)
print(f"Site: {site.extract_text()}")
```

## Extract the Summary

The summary requires navigating down from the label:

```python
summary = (
    page
    .find(text="Summary")
    .below(include_source=True, until='line')
)
summary.show(crop=True)
print(summary.extract_text())
```

# Extracting Tables

Natural PDF makes table extraction straightforward:

```python
table = page.extract_table()
df = table.to_df()
df
```

## Extracting Specific Tables

For pages with multiple tables, select the region first:

```python
# Find violations table by locating its header
violations_area = (
    page
    .find('text[size>10]:bold:contains("Violations")')
    .below(
        until='text:contains(Jungle Health)',
        include_endpoint=False
    )
)

# Extract table from that area
violations_df = violations_area.extract_table().to_df()
violations_df
```

# Exclusion Zones

When processing many similar documents, you can define areas to ignore (like headers and footers):

```python
# Define areas to exclude
top_header = page.region(top=0, left=0, height=80)
bottom_line = page.find_all("line")[-1].below()

# Add exclusions
page.add_exclusion(top_header)
page.add_exclusion(bottom_line)

# Visualize exclusions
page.show(exclusions='red')
```

Now extraction will ignore these areas:

```python
# Extract text without header/footer
clean_text = page.extract_text()
print(clean_text)
```

You can even add exclusions at the PDF level for multi-page documents:

```python
# Apply to all pages
pdf.add_exclusion(lambda page: page.region(top=0, left=0, height=80))
pdf.add_exclusion(lambda page: page.find_all("line")[-1].below())
```

# Key Takeaways

1. **Multiple selection methods**: CSS-like selectors, text search, color attributes
2. **Spatial navigation**: `.right()`, `.below()`, `.region()` for relative positioning
3. **Visual debugging**: `.show()` helps understand what you're selecting
4. **Table extraction**: Simple `.extract_table()` with region selection for complex cases
5. **Exclusion zones**: Define once, apply everywhere for consistent extraction