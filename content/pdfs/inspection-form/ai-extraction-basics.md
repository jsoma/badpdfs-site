---
slug: "ai-extraction-basics"
title: "AI Question Answering Basics"
description: "Using extractive question answering to pull information from PDFs"
pdf: "practice.pdf"
tags: ["workshop", "ai", "question-answering"]
---

# Let's ask questions

Time for some AI magic. We're using **extractive question answering**, which is different from LLMs because it pulls content *from the page*. LLMs are *generative AI*, which take your question and generates *new* text.

```python
from natural_pdf import PDF

pdf = PDF("practice.pdf")
page = pdf.pages[0]
page.show()
```

```python
result = page.ask("What date was the inspection?")
result
```

Notice it has a **confidence score**, which makes life great. You can also use `.show()` to see where it's getting the answer from.

```python
result.show()
```

It automatically doesn't show you answers it doesn't have much faith in.

```python
result = page.ask("Summary", min_confidence=0.0)

if result.found:
    print(result)
else:
    print("No answer found")
```

That does NOT mean it's always accurate, though. Using the words on the page makes it a lot easier. **Let's compare these two:**

```python
page.ask("How many violations were there?")
```

```python
page.ask("What was the violation count?")
```

You could also ask a series of questions and push them into a dataframe if you reaaaally want.

```python
answers = page.ask(['violation count', 'site', 'location'])
answers
import pandas as pd

pd.DataFrame(answers)
```

There are better ways to extract structured data, though.

## Structured data generation

### Using extractive Doc Q&A (same as `.ask`)

```python
from natural_pdf import PDF

pdf = PDF("practice.pdf")
page = pdf.pages[0]
```

```python
page.extract(["site", "date", "violation count", "inspection service", "summary", "city", "state"])
```

```python
page.extracted()
dict(page.extracted())
```

```python
page.extracted('city')
```

## Leveraging an LLM for structured data

Sometimes you want an opinion from an LLM, though. You want it to write things that aren't in there, or piece together something complicated. It's worth the potential for hallucinations!

Below we're using Google thanks to its [OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai).

```python
import os
from openai import OpenAI

# Initialize your LLM client
# Anything OpenAI-compatible works!
# Set your API key as an environment variable:
# export GEMINI_API_KEY="your_actual_api_key"
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),  # Get API key from environment
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Changes based on what AI you're using
)

fields = ["site", "date", "violation count", "inspection service", "summary", "city", "state"]
page.extract(fields, client=client, model="gemini-2.0-flash-lite") 
```

```python
dict(page.extracted())
```

### Very intense structured data extraction

Instead of being kind of loose and free with what you want, you can also get MUCH fancier and write a Pydantic model. It will not only send the column names you want, but also little descriptions and demands about strings (text), integers, floats and more.

You can find more details [here](https://platform.openai.com/docs/guides/structured-outputs).

```python
import os
from pydantic import BaseModel, Field
from openai import OpenAI

# Initialize your LLM client
# Anything OpenAI-compatible works!
# Set your API key as an environment variable:
# export GEMINI_API_KEY="your_actual_api_key"
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),  # Get API key from environment
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define your schema
class ReportInfo(BaseModel):
    inspection_number: str = Field(description="The main report identifier")
    inspection_date: str = Field(description="The name of the issuing company")
    inspection_service: str = Field(description="Name of inspection service")
    site: str = Field(description="Name of company inspected")
    summary: str = Field(description="Visit summary")
    city: str
    state: str = Field(description="Full name of state")
    violation_count: int

# Extract data
page.extract(schema=ReportInfo, client=client, model="gemini-2.0-flash-lite") 
```

```python
page.extracted()
```

Looks good, but...

```python
page.extracted('state')
```

Do you like how it still gives you an abbreviated state? Sigh, I don't know why it does it! So we can add a custom prompt to just be EXTRA sure about it.

```python
prompt = """Extract the information corresponding to the fields in the ReportInfo schema. 
If you find a state abbreviation be sure to expand it to the full state name.

- Washington instead of Wash. or WA
- California instead of Calif. or CA

Respond only with the structured data.
"""

page.extract(schema=ReportInfo, client=client, model="gemini-2.0-flash-lite", prompt=prompt) 
page.extracted()
```

```python
dict(page.extracted())
```

```python
page.extracted('state')
```

## Table extraction with LLMs

In the example below, we're saying "Using Gemini, provide a violations table - each row should have a statute, a description, a level, and a repeat-checked

```python
import os
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import List, Literal

# Set your API key as an environment variable:
# export GEMINI_API_KEY="your_actual_api_key"
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),  # Get API key from environment
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class ViolationsRow(BaseModel):
    statute: str
    description: str
    level: str
    repeat_checked: Literal["checked", "unchecked"] = Field("Whether the checkbox is checked or not")

class ViolationsTable(BaseModel):
    inspection_id: str
    violations: List[ViolationsRow]

page.extract(schema=ViolationsTable, client=client, model="gemini-2.0-flash-lite") 
```

Note that when we look below... **it didn't do the checked/unchecked correctly!**

```python
import pandas as pd

data = page.extracted()
pd.DataFrame(data.model_dump()['violations'])
```

...but that's because by default, the LLM uses the **text of the page**. What if we ask it to use **vision** instead of the default of **text**?

```python
page.extract(schema=ViolationsTable, client=client, model="gemini-2.0-flash-lite", using='vision') 

data = page.extracted()
pd.DataFrame(data.model_dump()['violations'])
```

I'll be honest: **I don't like that this even works.** Hallucinations are such a problem that we really need a better way to do this - because in this case we're not only relying on it for checkboxes, we're relying on it for allllll of the text.

## Figuring out how to manage those pesky checkboxes

```python
from natural_pdf import PDF

pdf = PDF("practice.pdf")
page = pdf.pages[0]
page.show(width=500)
```

We can use .extract_table() no problem to get *most* of the columns, but we really really want those checkboes!

```python
df = page.extract_table().to_df()
df
```

Let's find all of the boxes below the "Violations" header...

```python
boxes = (
    page
    .find(text='Violations')
    .below()
    .find_all('rect')
)

boxes.show(crop=True)
```

Let's go through each box: **do you have a line inside of you?**

```python
rect1 = boxes[1]
rect1.show(crop=True)
```

```python
# Checking for partial overlap in case it runs up against the borders
rect1.find('line', overlap='partial')
```

```python
rect2 = boxes[4]
rect2.show(crop=True)
```

```python
rect2.find('line', overlap='partial')
```

We can use `.apply` to go through each box and say 'yes' if there's a line, and 'no' otherwise.

```python
# I'll convert to a list so we can see the missing elements
list(
    page
    .find(text='Violations')
    .below()
    .find_all('rect')
    .find('line', overlap='partial')
)
```

```python
df['repeat'] = (
    page
    .find(text='Violations')
    .below()
    .find_all('rect')
    .find('line', overlap='partial')
    .apply(lambda e: 'checked' if e else 'unchecked')
)
df
```

## Classification

But what if it's an *image* of a rectangle that's checked or unchecked? No worries, AI to the rescue yet again! And this time it's a *local model*, something where you don't have to rely on ChatGPT or Anthropic or any of those.

I'm going to pull the boxes in by -1 pixels on each side so we can focus on the contents of the box.

```python
boxes = (
    page
    .find(text='Violations')
    .below()
    .find_all('rect')
    .expand(-1)
)
boxes.show(crop=True)
```

```python
boxes[0].show(crop=True)
```

What categories should we use? checked vs unchecked, X vs empty?

```python
boxes[0].classify(['checked', 'unchecked'], using="vision").category
```

```python
boxes[0].classify(['X', 'empty'], using="vision").category
```

```python
boxes[2].show(crop=True)
```

```python
boxes[2].classify(['X', 'empty'], using="vision").category
```

```python
(
    boxes
    .classify_all(['X', 'empty'], using="vision")
    .apply(lambda r: r.category)
)
```

```python
df['repeat'] = (
    boxes
    .classify_all(['X', 'empty'], using="vision")
    .apply(lambda r: r.category)
)
df
```

# Putting things in categories

## Categorizing an entire PDF

```python
from natural_pdf import PDF

pdf = PDF("practice.pdf")
page = pdf.pages[0]
page.show(width=500)
```

```python
pdf.classify(['slaughterhouse report', 'dolphin training manual', 'basketball', 'birding'], using='text')
pdf.category
```

```python
pdf.category_confidence
```

## Classifying pages of a PDF

Let's take a look at a document from the CIA investigating whether you can **use pigeons as spies**.

```python
from natural_pdf import PDF
