import pdfplumber

with pdfplumber.open("") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

# Save as .txt
with open("", "w") as f:
    f.write(text)
