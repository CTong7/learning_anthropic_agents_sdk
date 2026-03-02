---
name: pdf-parsing
description: Use this skill whenever you want to do anything with PDFs. to Call this tool whenever the user asks for you to interact with pdf files.
---

## Instructions

When the user asks about PDF content:
1. Use pdftotext to extract the PDF content
2. **IMPORTANT: After extracting the content, analyze it and provide a clear answer to the user's question**
3. Format your response in a clear, structured way

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout (recommended for structured documents)
pdftotext -layout input.pdf -

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5

# Extract the first 50 lines of the pdf
pdftotext input.pdf - | head -30
```