import unittest
import os
import tempfile
from file_scanner import extract_text_from_pdf, process_directory
from llama_handler import get_information_from_pdf

class TestPDFProcessor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.temp_dir, 'output.csv')

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_extract_text_from_pdf(self):
        # Create a sample PDF file for testing
        sample_pdf_path = os.path.join(self.temp_dir, 'sample.pdf')
        with open(sample_pdf_path, 'w') as f:
            f.write("Sample PDF content")
        
        extracted_text = extract_text_from_pdf(sample_pdf_path)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0)

    def test_process_directory(self):
        # Create a sample PDF file in the temp directory
        sample_pdf_path = os.path.join(self.temp_dir, 'sample.pdf')
        with open(sample_pdf_path, 'w') as f:
            f.write("Sample PDF content")
        
        process_directory(self.temp_dir, self.csv_file)
        self.assertTrue(os.path.exists(self.csv_file))

    def test_get_information_from_pdf(self):
        pdf_content = "Invoice\nNumber: 2024-08-01-01\nName: John Doe\nPrice: 100€\nDate: 21/02/2021"
        get_information_from_pdf(pdf_content, self.csv_file, "Pauline OLTMANNS", "test_file.pdf")
        self.assertTrue(os.path.exists(self.csv_file))

if __name__ == '__main__':
    unittest.main()