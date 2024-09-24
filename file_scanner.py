import os
import argparse
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from llama_handler import get_information_from_pdf
import logging

def setup_logging(log_level):
    """Set up logging configuration."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.error(f"Error processing {file_path}: {str(e)}")
        return ""

def process_directory(directory, csv_file, name, recursive=True, file_pattern='*.pdf'):
    """
    Processes a directory and extracts information from PDF files.
    
    :param directory: The directory to scan.
    :param csv_file: The CSV file to write the extracted information.
    :param name: The name to use in the LLaMA query.
    :param recursive: Whether to scan subdirectories.
    :param file_pattern: The file pattern to match (default: *.pdf).
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf') and fnmatch.fnmatch(file, file_pattern):
                file_path = os.path.join(root, file)
                logging.info(f"Processing: {file_path}")
                pdf_content = extract_text_from_pdf(file_path)
                if pdf_content:
                    get_information_from_pdf(pdf_content, csv_file, name, file_path)
        
        if not recursive:
            break  # Don't process subdirectories

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process PDF files in a directory and extract information.')
    parser.add_argument('directory', type=str, help='The directory to scan for PDF files.')
    parser.add_argument('csv_file', type=str, help='The CSV file to write the extracted information.')
    parser.add_argument('-n', '--name', type=str, default="Pauline OLTMANNS", help='The name to use in the LLaMA query (default: Pauline OLTMANNS)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Scan subdirectories recursively')
    parser.add_argument('-p', '--pattern', type=str, default='*.pdf', help='File pattern to match (default: *.pdf)')
    parser.add_argument('-l', '--log-level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                        default='INFO', help='Set the logging level')

    args = parser.parse_args()
    
    setup_logging(args.log_level)
    
    if not os.path.isdir(args.directory):
        logging.error(f"Error: {args.directory} is not a valid directory.")
    else:
        process_directory(args.directory, args.csv_file, args.name, args.recursive, args.pattern)