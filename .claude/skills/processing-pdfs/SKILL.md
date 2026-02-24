---
name: pdf-parsing
description: Use this skill whenever you want to do anything with PDFs. to Call this tool whenever the user asks for you to interact with pdf files.
---

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```