import os
import argparse
import shutil
from datetime import datetime
import colorama
from pdf_processor import extract_text_from_pdf
from document_analyzer import analyze_document
from file_organizer import organize_file

def setup_argparse():
    parser = argparse.ArgumentParser(
        description='Process PDF files and organize them based on extracted information.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_directory', type=str, help='The directory to scan for PDF files.')
    parser.add_argument('output_directory', type=str, help='The base directory to organize the files into.')
    parser.add_argument('--dry-run', action='store_true', help='Simulate the process without moving files.')
    parser.add_argument('--recursive', '-r', action='store_true', help='Scan subdirectories recursively.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output.')
    return parser

def process_file(file_path, output_directory, dry_run=False, verbose=False):
    """
    Processes a single PDF file and organizes it based on extracted information.
    
    :param file_path: Path to the PDF file.
    :param output_directory: The base directory to organize the file into.
    :param dry_run: If True, simulate the process without moving files.
    :param verbose: If True, print detailed information.
    """
    if verbose:
        print(colorama.Fore.CYAN + f"Processing: {file_path}" + colorama.Fore.RESET)
    
    try:
        # Extract text from PDF
        pdf_content = extract_text_from_pdf(file_path)
        
        if pdf_content:
            # Analyze document to extract required information
            doc_info = analyze_document(pdf_content)
            
            if doc_info:
                if dry_run:
                    print(colorama.Fore.YELLOW + f"[DRY RUN] Would move {file_path} based on:" + colorama.Fore.RESET)
                    for key, value in doc_info.items():
                        print(f"  {key}: {value}")
                else:
                    # Organize file based on extracted information
                    new_file_path = organize_file(file_path, output_directory, doc_info)
                    if verbose:
                        print(colorama.Fore.GREEN + f"File moved to: {new_file_path}" + colorama.Fore.RESET)
            else:
                print(colorama.Fore.RED + f"Could not extract required information from: {file_path}" + colorama.Fore.RESET)
        else:
            print(colorama.Fore.RED + f"Could not extract text from: {file_path}" + colorama.Fore.RESET)
    
    except Exception as e:
        print(colorama.Fore.RED + f"Error processing {file_path}: {str(e)}" + colorama.Fore.RESET)

def process_directory(input_directory, output_directory, dry_run=False, recursive=False, verbose=False):
    """
    Processes a directory and organizes PDF files based on extracted information.
    
    :param input_directory: The directory to scan for PDF files.
    :param output_directory: The base directory to organize the files into.
    :param dry_run: If True, simulate the process without moving files.
    :param recursive: If True, scan subdirectories recursively.
    :param verbose: If True, print detailed information.
    """
    if recursive:
        for root, _, files in os.walk(input_directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    process_file(file_path, output_directory, dry_run, verbose)
    else:
        for file in os.listdir(input_directory):
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(input_directory, file)
                process_file(file_path, output_directory, dry_run, verbose)

def main():
    colorama.init()
    parser = setup_argparse()
    args = parser.parse_args()

    if not os.path.isdir(args.input_directory):
        print(colorama.Fore.RED + f"Error: {args.input_directory} is not a valid directory." + colorama.Fore.RESET)
        return

    if not args.dry_run and not os.path.isdir(args.output_directory):
        print(colorama.Fore.YELLOW + f"Creating output directory: {args.output_directory}" + colorama.Fore.RESET)
        os.makedirs(args.output_directory, exist_ok=True)

    print(colorama.Fore.CYAN + "Starting PDF processing..." + colorama.Fore.RESET)
    process_directory(args.input_directory, args.output_directory, args.dry_run, args.recursive, args.verbose)
    print(colorama.Fore.GREEN + "PDF processing completed." + colorama.Fore.RESET)

if __name__ == "__main__":
    main()