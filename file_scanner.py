import os
import argparse

def scan_directory(directory):
    """
    Recursively scans a directory and prints all file paths.
    
    :param directory: The directory to scan.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scan a directory and print all file paths.')
    parser.add_argument('directory', type=str, help='The directory to scan.')

    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
    else:
        scan_directory(args.directory)
