# PDF Information Extractor

This project is designed to process PDF files, extract key information, and store it in a CSV file. It uses OCR capabilities when necessary and leverages the Llama model for information extraction.

## Table of Contents

1. [Installation](#installation)
2. [Running the Project](#running-the-project)
3. [Command-Line Options](#command-line-options)
4. [Running Unit Tests](#running-unit-tests)
5. [Global Usage](#global-usage)
6. [Project Structure](#project-structure)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pdf-information-extractor.git
   cd pdf-information-extractor
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Project

To process PDF files and extract information:

```
python file_scanner.py /path/to/pdf/directory output.csv
```

Replace `/path/to/pdf/directory` with the directory containing your PDF files, and `output.csv` with your desired output file name.

## Command-Line Options

The script supports the following command-line options:

```
usage: file_scanner.py [-h] [-n NAME] [-r] [-p PATTERN] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] directory csv_file

Process PDF files in a directory and extract information.

positional arguments:
  directory             The directory to scan for PDF files.
  csv_file              The CSV file to write the extracted information.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  The name to use in the LLaMA query (default: Pauline OLTMANNS)
  -r, --recursive       Scan subdirectories recursively
  -p PATTERN, --pattern PATTERN
                        File pattern to match (default: *.pdf)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level
```

Examples:

1. Process all PDF files in a directory and its subdirectories:
   ```
   python file_scanner.py /path/to/pdfs output.csv -r
   ```

2. Process only files matching a specific pattern:
   ```
   python file_scanner.py /path/to/pdfs output.csv -p "invoice*.pdf"
   ```

3. Set a custom name for the LLaMA query:
   ```
   python file_scanner.py /path/to/pdfs output.csv -n "John Doe"
   ```

4. Set the logging level to DEBUG:
   ```
   python file_scanner.py /path/to/pdfs output.csv -l DEBUG
   ```

## Running Unit Tests

To run the unit tests:

```
python -m unittest test_pdf_processor.py
```

This will execute all the test cases defined in the `test_pdf_processor.py` file.

## Global Usage

The PDF Information Extractor consists of several components working together:

1. `file_scanner.py`: This is the main entry point. It scans the specified directory for PDF files, extracts text from them (using OCR if necessary), and calls the Llama model to extract relevant information.

2. `llama_handler.py`: This file contains the logic for interacting with the Llama model. It sends the extracted PDF content to the model and processes the response.

3. `csv_handler.py`: This file handles the creation and updating of the CSV file with the extracted information.

The general flow of the application is as follows:

1. The user specifies a directory, an output CSV file, and optional parameters using command-line arguments.
2. The application scans the directory (and subdirectories if specified) for PDF files matching the given pattern.
3. For each matching PDF file:
   a. The text is extracted (using OCR if needed).
   b. The extracted text is sent to the Llama model.
   c. The model extracts key information (number, name, price, date).
   d. The extracted information is written to the CSV file.

## Project Structure

```
pdf-information-extractor/
│
├── file_scanner.py
├── llama_handler.py
├── csv_handler.py
├── test_pdf_processor.py
├── requirements.txt
└── README.md
```

- `file_scanner.py`: Main script for scanning directories and processing PDFs
- `llama_handler.py`: Handles interaction with the Llama model
- `csv_handler.py`: Manages CSV file operations
- `test_pdf_processor.py`: Contains unit tests
- `requirements.txt`: Lists all Python dependencies
- `README.md`: This file, containing project documentation

## Note

Ensure that you have the necessary permissions to read the PDF files and write to the output CSV file. Also, make sure you have set up and configured the Llama model correctly as per the `ollama` library documentation.