import pypdf

def extract_text(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    pdf_file = "amplifier_content.pdf"
    content = extract_text(pdf_file)
    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Text saved to extracted_text.txt")
