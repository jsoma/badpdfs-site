---
slug: "cia-document-extraction"
title: "CIA Document Analysis"
description: "Extracting information from declassified CIA documents using AI"
pdf: "cia-doc.pdf"
tags: ["workshop", "ai", "government-documents"]
published: true
---

# CIA Document Classification

Let's work with a declassified CIA document and use AI to classify and extract information.

```python
from natural_pdf import PDF

pdf = PDF("cia-doc.pdf")
pdf.pages.show(cols=6)
```

Just like we did above, we can ask what category we think the PDF belongs to.

```python
pdf.classify(['slaughterhouse report', 'dolphin training manual', 'basketball', 'birding'], using='text')
(pdf.category, pdf.category_confidence)
```

But notice how all of the pages look very very different: **we can also categorize each page using vision**.

```python
pdf.classify_pages(['diagram', 'text', 'invoice', 'blank'], using='vision')

for page in pdf.pages:
    print(f"Page {page.number} is {page.category} - {page.category_confidence:0.3}")
```

And if we just want to see the pages that are diagrams, we can `.filter` for them.

```python
(
    pdf.pages
    .filter(lambda page: page.category == 'diagram')
    .show(show_category=True)
)

```

We can also put them into groups.

```python
groups = pdf.pages.groupby(lambda page: page.category)
groups.info()
```

```python
diagrams = groups.get('diagram')
diagrams.show()
```

And if that's all we're interested in? We can save a new PDF of just those pages!

```python
(
    pdf.pages
    .filter(lambda page: page.category == 'diagram')
    .save_pdf("diagrams.pdf", original=True)
)
```