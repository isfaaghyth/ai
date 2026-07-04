---
name: pdf-summarizer
description: Extracts text from a PDF file and generates a structured summary.
version: 1.0.0
author: Your Name
metadata:
  hermes:
    tags: [productivity, pdf, tools]
---

# PDF Summarizer Instructions
When a user asks to summarize a PDF file, follow these steps:
1. Locate the absolute path of the PDF.
2. Run the helper Python script using the shell executor tool:
   `python3 /opt/data/skills/productivity/pdf-summarizer/scripts/summarize.py --file "/path/to/document.pdf"`
3. Present the resulting structured summary back to the user.
