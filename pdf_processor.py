import PyPDF2
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyPDF2 and OCR if necessary.
    
    :param file_path: Path to the PDF file.
    :return: Extracted text from the PDF.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        
        if not text.strip():  # If no text was extracted, use OCR
            images = convert_from_path(file_path)
            for image in images:
                text += pytesseract.image_to_string(image)
        
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {str(e)}")
        return ""