from pypdf import PdfReader

def read_pdf_content(file_path):

    try:
        reader =  PdfReader(file_path)

        pdf_content = ""

        for page in reader.pages:
            page_content = page.extract_text()

            if page_content:
                pdf_content += page_content + "\n"

        return pdf_content

    except Exception as e:
        print(f"Error: {e}. Unable to read the file.")
        return ""