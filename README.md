# HW4: Co-Actor Network Scraper

**Name:** Hansen Yang
**Course:** DS3500

---

## 1. Project Description

<!-- 
Briefly describe your project:
- Which two actors did you choose? Jackie Chan and Leonardo DiCaprio
- Which three websites did you scrape? Wikipedia IMDb Allmovie
- How many rows of data did you end up with? How much data were you able to scrape from each of the three websites?
-->

For wikipedia, I got 931 rows for Jackie Chan and Leonardo DiCaprio
But I failed for both IMDb and allmovie

---

## 2. Robots.txt Analysis

<!-- 
For each of your three sites, write 2-3 sentences covering:
- What does the site's robots.txt allow or disallow for scrapers?
- Was your scrape within those bounds? Why or why not?
-->

### Wikipedia

The robots.txt file make me to access Wikipedia article pages but prevents access to 
various dynamic and special content paths, which include the directories w and api
My scraping activities remained within established site boundaries since I 
obtained standard article content through actor filmography and individual movie page requests

### IMDb

The robots.txt file of IMDb prohibits access to multiple search-related websites, which include both searchtitle and
 search name paths and other restricted sections.  I did not use IMDb search functions
and I tried to access direct person pages, but my requests produced unexpected results 
because they failed to show the links that I needed, so I did not try to work around

### Allmovies

My AllMovie scrape failed because the actor profile URLs redirected 
to search pages, which the site robots.txt file prevented Scrapy from accessing,
site allowed only restricted access to its content

---

## 4. Scraping Reflection

<!--
For each site, briefly describe:
- How easy or hard was it to scrape?
- Did you succeed, partially succeed, or fail? Why?
-->

### Wikipedia

The Wikipedia site is an esay online resource for web scraping purposes
Film pages present their content in an organized structure which enables extraction of co-actor details through
the special movie pages that feature structured infobox fields for release date and director and starring actors

### IMDb

IMDb became the most challenging website throughout the entire project,
I tryed and it does not work out, the scrape get no outputs

### Allmovies

AllMovie was not successful also, the actor profile URLs redirected to search pages,
and those redirected pages were blocked by robots.txt in my Scrapy

---

## 5. AI Usage

<!-- 
If you did NOT use generative AI, write: "I did not use generative AI for this assignment."
If you DID use generative AI, complete all four subsections below.
-->

### Prompt Log

<!--
Summarize the prompts you used, in order.
You don't need to copy-paste exact prompts -- a sentence or two describing each is fine.
-->

I used AI to help me understand the work, 
used it to generate starter versions of the spiders, make me know what should I do,
explain error messages, and suggest debugging steps for project structure

### What Broke

<!--
What did the AI get wrong? How did you identify it? How did you fix it?
-->

AI make some errors in the code, that the names files are in the wrong name
some selectors does not match and I change it

### Code Ownership

<!--
For each major component of your project, note whether you:
- Wrote it yourself
- Accepted it from AI output with no changes
- Modified AI output

A table works well here. Example:

| Component            | Ownership                        |
|----------------------|----------------------------------|
| Scrapy logic         | Modified from AI output          |
| Website parse logic  | AI for all three sites           |
| Pipeline / output    | Accepted from AI                 |
| settings.py config   | Wrote myself                     |
-->

| Component | Ownership |
|Scrapy logic| Myself|
|website logic | Helped by AI|
|pipeline | myself|
| setting | myself and use AI to fix problem|


### Reflection

<!--
In 3-5 sentences: What would you have done differently if you couldn't use AI?
Do you feel like using AI cost you in terms of understanding?
-->

AI saved some time for my work and gives me a better understanding of the
project, let me be more efficent and know how I get wrong with the code, 
help me to debug easily. SOME suggested selectors and spider logic
did not match the actual sites, so I needed to debug through all parts of the code to track
its complete functionality, but its is still helpful.