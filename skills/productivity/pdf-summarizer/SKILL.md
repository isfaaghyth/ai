---
name: pdf-summarizer
description: Extracts text from a PDF file so the agent can generate a structured summary.
version: 1.0.0
author: Isfa
metadata:
  hermes:
    tags: [productivity, pdf, tools]
---

# PDF Summarizer Instructions

When a user asks to summarize a PDF file, follow these steps:

1. Locate the absolute path of the PDF.
2. Verify that `pypdf` is installed. If not, run:
   `pip install -r /opt/data/skills/productivity/pdf-summarizer/requirements.txt`
3. Run the helper Python script using the shell executor tool:
   `python3 /opt/data/skills/productivity/pdf-summarizer/scripts/summarize.py --file "/path/to/document.pdf"`
4. Read the printed raw text output.
5. Apply your reasoning model to generate a structured, bulleted summary of the text and present it back to the user.
