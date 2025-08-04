---
slug: czech-republic-pisa2012_zakovsky_dotaznik_a
title: Complex Table Extraction from OECD Czech PISA Assessment
description: This PDF is a document from the OECD regarding the PISA assessment, provided
  in Czech. The main extraction goal is to get the survey question table found on
  page 9. Challenges include the weird table format, making it hard to extract automatically.
pdf: czech-republic-pisa2012_zakovsky_dotaznik_a.pdf
tags:
- OECD
- Czech
- PISA
- Survey Table
- Complex Format
file_size_mb: 0.86
page_count: 56
submitted_by: Yuqi Liao
language: Czech
published: true
---
# Complex Table Extraction from OECD Czech PISA Assessment

This PDF is a document from the OECD regarding the PISA assessment, provided in Czech. The main extraction goal is to get the survey question table found on page 9. Challenges include the weird table format, making it hard to extract automatically.

I'm assuming by "survey question" the submitter wants *as much as possible*. You can extend the work we do here to get all of the surveys in the PDF, but for now we're just going to do a single section of the survey, from pages 7-15.

```python
from natural_pdf import PDF

pdf = PDF("czech-republic-pisa2012_zakovsky_dotaznik_a.pdf")
pdf.pages[6:15].show()
```

If we want to look at one of the pages, it seems like the questions are in bold.

```python
pdf.pages[7].find_all("text:bold:not-empty").show()
```

Zoom in! You can see that some of the words, like vzdělání, are broken up into *multiple words*. We can see why if we inspect the text on the page.

```python
pdf.pages[7].inspect()
```

Turns out the accented letters are a font variant! Each change in boldness, font size, or font type trigger the idea that something is a *new word*, even if we know it's not.

Do we deal with it? Do we ignore it? At least two paths open up ahead!

/// tab | Dissolving and `.find_all`
By default we'll assume you don't know why this is happening, and lean heavily in `dissolve()`. Dissolve can be used to combine texts or regions that are close to one another.

```python
pdf.pages[7].find_all("text:bold:not-empty").dissolve().show()
```

When we use `dissolve()` on the selection you'll see them combine into blocks. Along with weird font issues, dissolving is also useful for combining parts of the same question that are broken into separate rows. By using `padding=5` we have the dissolve reach out five pixels to find nearby overlapping regions, including the ones on the row above/below.

```python
questions = (
    pdf
    .pages[6:15]
    .find_all('text:bold[size~=14][x0>100]:not-empty')
    .dissolve(padding=5)
)
questions.show()
```

If we were just interested in the questions, we could pull them each out now.

```python
questions.extract_each_text()
```

Instead, we're going to use the question to **break the page into sections**. Starting from each question, we'll look `.below()` until it hits the either:

- The next question
- A wide line (Why is it a `rect`? Who knows!)
- The STXX text used to denote questions

This didn't come easy: It took a lot of trial and error to see the right selectors.

```python
answer_areas = (
    questions.below(
        until='text:bold[size~=14]:regex(\d+) | rect[width>300] | text:regex(^ST\d)',
        include_endpoint=False
    )
)
answer_areas.show()
```

Now we can find the text of the question by asking for the text that is neither bold nor tiny:

```python
answer_areas[3].find_all('text:not(:italic):not-empty[size>8]').show()
```

And if we want it for each of the questions, we'll just search through each of them.

> There are about two hundred ways to do this part.

```python
results = []
for question, answer_area in zip(questions, answer_areas):
    result = {}
    result['question'] = question.extract_text()
    result['notes'] = (
        answer_area
        .find_all('text:italic:not-empty[size>8]')
        .extract_text()
    )
    result['answers'] = (
        answer_area
        .find_all('text:not(:italic):not-empty[size>8]')
        .extract_text()
    )
    results.append(result)
print("Found", len(results))
```

Now we can pack it up into pandas and be good to go.

```python
import pandas as pd

df = pd.DataFrame(results)
df
```
///

/// tab | Breaking into sections

Instead of focusing on the questions, we can also think about patterns on the page: each question begins with a number. Let's break the page up based on bold, size 14 text that includes numbers.

```python
sections = (
    pdf
    .pages[6:15]
    .get_sections(
        start_elements='text:bold[size~=14]:regex(\d+)'
    )
)
sections.show()
```

Let's a look at the first section.

```python
sections[0].show()
```

If we wanted the rough text from the section, we just ask for it.

```python
text = sections[0].extract_text(layout=True)
print(text)
```

Most likely we want to pull out the pieces separately: the italic, the bold, the normal. We can inspect the text on the page to see what selectors might work for each.

```python
sections[0].find_all('text').inspect()
```

```python
question = sections[0].find_all('text:bold').extract_text()
print(question)
```

```python
notes = sections[0].find_all('text:italic[size~=14]').extract_text()
print(notes)
```

```python
answers = (
    sections[0]
    .find_all('text:not(:bold):not(:italic)[size=12]')
    .extract_text(
        layout=True,
        strip=True,
    )
)
print(answers)
```

Now that we know it works for one of them, we can do it for all of the sections.

```python
results = []

for section in sections:
    question = (
        section
        .find_all('text:bold')
        .extract_text()
    )
    notes = (
        section
        .find_all('text:italic[size~=14]')
        .extract_text()
    )
    answers = (
        section
        .find_all('text:not(:bold):not(:italic)[size=12]')
        .extract_text(layout=True, strip=True)
    )
    results.append({
        'question': question,
        'notes': notes,
        'answers': answers
    })
len(results)
```

Pop it into a pandas dataframe and you're ready to go!

```python
import pandas as pd

df = pd.DataFrame(results)
df.head()
```
///

Done!