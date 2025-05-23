# AI powered pdf sorter

This project is designed to process PDF files, extract key information, and organize them based on the extracted data. It uses OCR capabilities when necessary and leverages the Llama model for information extraction.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Command-Line Options](#command-line-options)
5. [Document Types](#document-types)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
8. [License](#license)

## Features

- Extract text from PDF files (with OCR support for scanned documents)
- Analyze documents to extract key information:
  - Date
  - Document type
  - Emitter
  - Recipient
- Organize files based on extracted information
- Colored console output for better readability
- Dry run capability to simulate processing without moving files
- Recursive directory scanning option

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Ovsiankina/ai-powered-pdf-sorter.git
   cd ai-powered-pdf-sorter
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required python dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Install the required system depedencies:
```
# On arch linux:
sudo pacman -S tesseract tesseract-data-eng ollama
```

5. Initiate Ollama:
```
ollama serve

# In another terminal
ollama pull <ollamanModel>
```

By default, the app uses the Ollama Model "Llama3.2".
You can change it to whatever Ollama model you'd like as long as it supports
tools.

To modify the model, change the calue of the `ollamaModel` variable on line 17 
of `./document_analyzer.py`.

6. Keep ollama running in the background with `ollama serve` and run the app. 

## Usage

To process PDF files and extract information:

```
python main.py /path/to/pdf/directory /path/to/output/directory
```

Replace `/path/to/pdf/directory` with the directory containing your PDF files, and `/path/to/output/directory` with your desired output directory.

## Command-Line Options

The script supports the following command-line options:

```
usage: main.py [-h] [--dry-run] [--recursive] [--verbose] input_directory output_directory

Process PDF files and organize them based on extracted information.

positional arguments:
  input_directory   The directory to scan for PDF files.
  output_directory  The base directory to organize the files into.

optional arguments:
  -h, --help        show this help message and exit
  --dry-run         Simulate the process without moving files.
  --recursive, -r   Scan subdirectories recursively.
  --verbose, -v     Enable verbose output.
```

Examples:

1. Process all PDF files in a directory and its subdirectories:
   ```
   python main.py /path/to/pdfs /path/to/output --recursive
   ```

2. Perform a dry run to see what would happen without actually moving files:
   ```
   python main.py /path/to/pdfs /path/to/output --dry-run
   ```

3. Enable verbose output for detailed information:
   ```
   python main.py /path/to/pdfs /path/to/output --verbose
   ```

## Document Types

The system recognizes the following document types:

- `facture`: A bill or invoice for goods or services
- `devis`: A quote or estimate for goods or services
- `mail`: An email or written correspondence
- `arrêt maladie`: A medical certificate or sick leave document
- `impots`: Tax-related documents or forms
- `relevé de comptes`: Bank statement or account summary
- `autres`: Any other type of document not fitting the above categories

## Project Structure

```
pdf-information-extractor/
│
├── main.py
├── document_analyzer.py
├── file_organizer.py
├── pdf_processor.py
├── requirements.txt
└── README.md
```

- `main.py`: Main script for scanning directories and processing PDFs
- `document_analyzer.py`: Handles document analysis and information extraction
- `file_organizer.py`: Manages file organization based on extracted information
- `pdf_processor.py`: Handles PDF text extraction (including OCR)
- `requirements.txt`: Lists all Python dependencies
- `README.md`: This file, containing project documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
