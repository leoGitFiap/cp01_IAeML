from pypdf import PdfReader

def read_file_content(file_path):

    try:
        reader =  PdfReader(file_path)

        file_content = ""

        for page in reader.pages:
            page_content = page.extract_text()

            if page_content:
                file_content += page_content + "\n"

        return file_content

    except Exception as e:
        print(f"Error: {e}. Unable to read the file.")
        return ""