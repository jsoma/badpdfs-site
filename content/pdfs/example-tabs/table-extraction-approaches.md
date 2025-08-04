---
slug: table-extraction-approaches
title: Multiple Approaches to Table Extraction
description: Demonstrating different ways to extract tables from PDFs using natural-pdf, from basic text extraction to advanced AI-powered methods
pdf: sample-table.pdf
tags:
- Table Extraction
- Multiple Approaches
- AI Extraction
- Pandas Integration
file_size_mb: 0.5
page_count: 2
submitted_by: Demo
---

# Multiple Approaches to Table Extraction

This example demonstrates three different approaches to extracting tables from PDFs, each with different trade-offs between simplicity, accuracy, and structure preservation.

/// tab | Basic Text Extraction
This approach uses simple text extraction - fast but may lose table structure.

```python
from natural_pdf import PDF

# Load the PDF
pdf = PDF("sample-table.pdf")
page = pdf.pages[0]

# Extract raw text
text = page.text
print("Raw text extraction:")
print(text)

# Try to identify table-like patterns
lines = text.split('\n')
for line in lines:
    if '\t' in line or '  ' in line:  # Possible table row
        print(f"Possible row: {line}")
```

**Pros:**
- Very fast
- Works with any PDF
- No dependencies

**Cons:**
- Loses table structure
- Difficult to parse complex tables
- Column alignment often lost
///

/// tab | Structured Table Detection
    select: true
Using natural-pdf's table detection to preserve structure and convert to pandas.

```python
from natural_pdf import PDF
import pandas as pd

# Load the PDF
pdf = PDF("sample-table.pdf")
page = pdf.pages[0]

# Extract tables with structure preserved
tables = page.extract_tables()
print(f"Found {len(tables)} tables")

# Convert first table to pandas DataFrame
if tables:
    df = tables[0].to_pandas()
    print("\nTable as DataFrame:")
    print(df)
    
    # Show basic statistics
    print("\nTable info:")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Display nicely formatted
    print("\nFormatted table:")
    print(df.to_string(index=False))
```

**Pros:**
- Preserves table structure
- Easy conversion to pandas
- Handles complex tables well

**Cons:**
- May miss tables with unusual formatting
- Slower than text extraction
///

/// tab | AI-Powered Extraction
Advanced extraction using AI to understand table context and meaning.

```python
from natural_pdf import PDF

# Load the PDF
pdf = PDF("sample-table.pdf")
page = pdf.pages[0]

# Use AI to understand and extract the table
result = page.ask("""
Extract the table from this page. 
Format it as a clean CSV with proper headers.
Also provide a summary of what the table contains.
""")

print("AI-extracted table:")
result.show()

# Get specific insights
insights = page.ask("""
What are the key insights from this table?
Are there any notable trends or outliers?
""")

print("\nKey insights:")
insights.show()
```

**Pros:**
- Understands context and meaning
- Can handle complex or damaged tables
- Provides insights beyond raw data

**Cons:**
- Requires AI/LLM access
- Slower than other methods
- May require prompt tuning
///

## Choosing the Right Approach

The best approach depends on your specific needs:

1. **Use Basic Text** when:
   - You need maximum speed
   - Tables have simple structure
   - You're doing initial exploration

2. **Use Table Detection** when:
   - You need structured data
   - Converting to pandas/CSV
   - Tables have clear boundaries

3. **Use AI Extraction** when:
   - Tables are complex or damaged
   - You need semantic understanding
   - Context and insights matter