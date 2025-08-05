---
slug: "ocr-example"
title: "OCR and AI magic"
description: "Master OCR techniques with Natural PDF - from basic text recognition to advanced LLM-powered corrections. Learn to extract text from image-based PDFs, handle tables without proper boundaries, and leverage AI for accuracy improvements."
pdf: "needs-ocr.pdf"
tags:
- OCR
- LLM Integration
- Text Extraction
- Table Detection
- AI Correction
file_size_mb: 0.5
page_count: 1
submitted_by: Natural PDF Team
published: true
---

# OCR: Recognizing text

Sometimes you can't actually get the text off of the page. It's an *image* of text instead of being actual text.

```python
from natural_pdf import PDF

pdf = PDF("ocr-example.pdf")

page = pdf.pages[0]
page.show(width=700)
```

Looks like it's full of text, right? But when we try to extract the text...

```python
text = page.extract_text()
print(text)
```

Nothing! **It's time for OCR.**

There are a looooot of OCR engines out there, and one of the things that makes Natural PDF nice is that it supports multiples. Figuring out which one is the "best" isn't as tough when you can just run them all right after each other.

The default is [EasyOCR](https://github.com/JaidedAI/EasyOCR) which usually works fine.

```python
page.apply_ocr()
```

```python
text = page.extract_text()
print(text)
```

I'm very iritated by the "Durham's Pure Leaf Lardl" instead of "Durham's Pure Leaf Lard!". Why'd it miss that??

I don't need to know why, though, really, because I can just try some other engine! You can also fool around with the options - some of the the lowest-hanging fruit is increasing the resolution of the OCR. The default at the moment is 150, you can try upping to 300 for (potentially) better results.

```python
page.apply_ocr('surya', resolution=192)
```

```python
text = page.extract_text()
print(text)
```

## Finding tables on OCR documents

When we used `page.extract_table()` last time, it was easy because there were all of these `line` elements on the page that pdfplumber could detect and say "hey, it's a table!" For the same reason that there's no *real* text on the page, there's also no *real* lines on the page. Instead, we're going to do a fun secret trick where we look at what horizontal and vertical coordinates *seem* like they might be lines by setting a threshold.

```python
page.extract_table()
```

```python
table_area = (
    page
    .find('text:contains(Violations)')
    .below(
        until='text:contains(Jungle)',
        include_endpoint=False
    )
)
table_area.show(crop=True)
```

```python
from natural_pdf.analyzers import Guides

guides = Guides(table_area)

# Add guides between the headers
guides.vertical.from_content(
    ['Statute', 'Description', 'Level', 'Repeat'],
    align='between'
)

# Shift them around so they don't overlap the text
guides.vertical.snap_to_whitespace(detection_method='text')

# add in horizontal lines in places where 80% of the pixels are 'used'
guides.horizontal.from_lines(threshold=0.8)

# Honestly you could have done the same thing for the vertical lines
# but it isn't as fun as .from_content, you know?
# n=5 finds the 5 most likely places based on pixel density
# guides.vertical.from_lines(n=5)

guides.show()
```

You can just extract the data with `.extract_table()`...

```python
df = guides.extract_table().to_df()
df
```

```python
df.to_csv("output.csv", index=False)
```

But if you want to actually do things with specific columns or have more control, you can ask the guides for specific columns or rows.

```python
guides.columns[-1].show()
```

```python
guides.rows[3].show()
```

### Figuring out information about things that are *not* text

In a tiny preview of the next notebook: **what about those checkboxes?** Turns out we can use **image classification AI** to do it for us!

```python
last_col = guides.columns[-1].expand(top=-40)
last_col.show(crop=True)
```

```python
cells = guides.cells[-1][:]
cells = cells.expand(left=-60, right=-175, top=-16, bottom=-16)
cells.show(crop=True)
```

```python
cells.classify_all(['X', 'empty'], using='vision')
```

```python
cells.apply(lambda cell: (cell.category, cell.category_confidence))
```

It's like magic! We'll look at it more in another notebook.

## Correcting OCR

While we love OCR when it works, it often does *not* work great. We have a few solutions: send humans after it, or use LLMs or spell check to correct it.

### With LLMs

Let's OCR at a low resolution, then see what our text looks like.

```python
page.apply_ocr(resolution=50)
page.find_all('text').inspect()
```

Some of these are pretty easy - for example, "Uraanilary Warking Conditions" should be "Unsanity working conditions." OCR tools just don't know that kind of thing! But what if we could go through each piece of text, some some sort of spell check or something?

You can use `correct_ocr` to change the text in a region.

```python
def correct_text_region(region):
    return "This is the updated text"
    
page.correct_ocr(correct_text_region) 
```

And then, magically, all of our text is whatever we `return`.

```python
page.find_all('text').inspect()
```

But clearly we don't want the same thing every time! Let's add the bad OCR back in...

```python
# Re-apply the OCR to break it again
page.apply_ocr('surya', resolution=15)
```

...and feed each line to an LLM trying to fix it.

```python
import os
from openai import OpenAI
from natural_pdf.ocr.utils import direct_ocr_llm

# Set your API key as an environment variable:
# export OPENAI_API_KEY="your_actual_api_key"
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

prompt = """
Correct the spelling of this OCR'd text, a snippet of a document.
Preserve original capitalization, punctuation, and symbols. 
Changing meaning is okay if it's clearly an OCR issue.
Do not add any explanatory text, translations, comments, or quotation marks around the result.
"""

def correct_text_region(region):
    text = region.extract_text()
    completion = client.chat.completions.create(
        model="gpt-4o-nano",
        messages=[
            {
                "role": "system", "content": prompt
            },
            {
                "role": "user",
                "content": text
            },
        ],
    )

    updated = completion.choices[0].message.content

    if text != updated:    
        print(f"OLD: {text}\nNEW:{updated}") 

    return updated

page.correct_ocr(correct_text_region) 
```

And now we can use `.extract_text()` the magicaly same way.

The real benefit of this vs sending the whole document to the LLM is *we don't change where the text is*. An LLM might OCR something for us, but it *loses the spatial context that we find so important*.

```python
text = page.extract_text()
print(text)
```

## Let's do the OCR with the LLM, period

But if the LLM is *that good* at OCR, we can also find pieces of the page we would like to OCR and *send them each in isolation to the LLM*. We use `detect_only=True` so it doesn't try to figure out what the text is, just that the text is there.

```python
page.apply_ocr('surya', detect_only=True)
page.find_all('text').show()
```

```python
page.find_all('text').inspect()
```

Now we'll do an even fancier `correct_text_region`: it takes the region as an image, and sends it right on over to the LLM for OCR.

```python
import os
from openai import OpenAI
from natural_pdf.ocr.utils import direct_ocr_llm

# Set your API key as an environment variable:
# export OPENAI_API_KEY="your_actual_api_key"
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

prompt = """OCR this image patch. Return only the exact text content visible in the image. 
Preserve original spelling, capitalization, punctuation, and symbols.
Fix misspellings if they are the result of blurry or incorrect OCR.
Do not add any explanatory text, translations, comments, or quotation marks around the result.
If you cannot process the image or do not see any text, return an empty space.
The text is from an inspection report of a slaughterhouse."""
# The text is likely from a Greek document, potentially a spreadsheet, containing Modern Greek words or numbers

def correct_text_region(region):
    # Use a high resolution for the LLM call for best accuracy
    return direct_ocr_llm(
        region, 
        client, 
        prompt=prompt, 
        resolution=150, 
        model="gpt-4o" 
    )

page.correct_ocr(correct_text_region) 
```

What do we have now?

```python
page.find_all('text').inspect()
```

```python
text = page.extract_text()
print(text)
```
