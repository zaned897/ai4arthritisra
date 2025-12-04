import pypdf

def extract_pages(source_path, output_path, page_indices):
    try:
        reader = pypdf.PdfReader(source_path)
        writer = pypdf.PdfWriter()

        for index in page_indices:
            if 0 <= index < len(reader.pages):
                writer.add_page(reader.pages[index])
            else:
                print(f"Warning: Page index {index} is out of bounds.")

        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"Successfully created {output_path}")

    except FileNotFoundError:
        print(f"Error: File not found at {source_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    source_file = "Memorias+del+Congreso+Celaya+2016+-+Tomo+34.pdf"
    output_file = "amplifier_content.pdf"
    # Pages 106-111 correspond to indices 105-110 (0-indexed)
    pages_to_extract = list(range(105, 111)) 
    
    extract_pages(source_file, output_file, pages_to_extract)
