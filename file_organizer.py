import os
import shutil
from datetime import datetime

def organize_file(file_path, output_directory, doc_info):
    """
    Organizes the file based on extracted information.
    
    :param file_path: Path to the original file.
    :param output_directory: Base directory for organized files.
    :param doc_info: Dictionary containing extracted document information.
    :return: Path to the new file location.
    """
    try:
        # Extract information
        date = datetime.strptime(doc_info['date'], "%Y-%m-%d")
        doc_type = doc_info['type']
        emitter = doc_info['emitter']
        recipient = doc_info['recipient']

        # Create directory structure
        new_dir = os.path.join(output_directory, doc_type, date.strftime("%Y-%m"))
        os.makedirs(new_dir, exist_ok=True)

        # Create new filename
        file_name = os.path.basename(file_path)
        new_file_name = f"{emitter} - {recipient} - {file_name}"
        new_file_path = os.path.join(new_dir, new_file_name)

        # Move the file
        shutil.move(file_path, new_file_path)

        return new_file_path
    except Exception as e:
        print(f"Error organizing file {file_path}: {str(e)}")
        return None