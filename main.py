import os
import argparse
import shutil
from datetime import datetime
from pdf_processor import extract_text_from_pdf
from document_analyzer import analyze_document
from file_organizer import organize_file

def process_directory(input_directory, output_directory):
    """
    Recursively processes a directory and organizes PDF files based on extracted information.
    
    :param input_directory: The directory to scan for PDF files.
    :param output_directory: The base directory to organize the files into.
    """
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                process_file(file_path, output_directory)

def process_file(file_path, output_directory):
    """
    Processes a single PDF file and organizes it based on extracted information.
    
    :param file_path: Path to the PDF file.
    :param output_directory: The base directory to organize the file into.
    """
    print(f"Processing: {file_path}")
    
    try:
        # Extract text from PDF
        pdf_content = extract_text_from_pdf(file_path)
        
        if pdf_content:
            # Analyze document to extract required information
            doc_info = analyze_document(pdf_content)
            
            if doc_info:
                # Organize file based on extracted information
                new_file_path = organize_file(file_path, output_directory, doc_info)
                print(f"File moved to: {new_file_path}")
            else:
                print(f"Could not extract required information from: {file_path}")
        else:
            print(f"Could not extract text from: {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")


parser = argparse.ArgumentParser(description='Process PDF files and organize them based on extracted information.')
parser.add_argument('input_directory', type=str, help='The directory to scan for PDF files.')
parser.add_argument('output_directory', type=str, help='The base directory to organize the files into.')

args = parser.parse_args()

if not os.path.isdir(args.input_directory):
    print(f"Error: {args.input_directory} is not a valid directory.")
elif not os.path.isdir(args.output_directory):
    print(f"Error: {args.output_directory} is not a valid directory.")
else:
    process_directory(args.input_directory, args.output_directory)