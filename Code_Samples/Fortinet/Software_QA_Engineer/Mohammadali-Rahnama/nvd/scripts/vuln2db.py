"""
NVD Vulnerability to Database Script
------------------------------------

This script extracts data from National Vulnerability Database (NVD) JSON files and saves it to a database.

Usage:
- Run the script with one or more NVD JSON file paths as command line arguments.
- The script will extract data from each file and save it to the specified database.
- Logging information is recorded for each file.

Requirements:
- Python 3.x

Folder Structure:
- nvd/
    - lib/
        - NVD.py
        - Log.py
    - scripts/
        - nvd_vuln2db.py

Modules:
- NVD: Module for NVD data extraction and database operations.
- Log: Module for setting up logging functionality.

Usage:
- Execute the script from the 'scripts' folder with the command: python nvd_vuln2db.py [./download/file1.json] [./download/file2.json] ...
- Provide one or more NVD JSON file paths as command line arguments.
- The script will extract data from each file and save it to the specified database.
- Logging information is recorded for each file.

"""

import os
import sys

# Add the project root directory to the system path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# Now, perform the import
from lib import NVD
from lib import Log

# setup logger (Folder, File name, Logger Name)
logger_vuln2db = Log.setup_log("log", "nvd", "vuln2db")

def print_usage():
    logger_vuln2db.warning("Usage: python nvd_extract.py [./download/file1.json] [./download/file2.json] ...")
    logger_vuln2db.warning("Please provide one or more NVD JSON file paths as command line arguments.")

def main():
    # Print usage information if no arguments are provided
    if len(sys.argv) < 2:
        print_usage()
        return
    else:
        # Add the database info here
        db_file = "nvd.db"
        db_table = "nvd_entries"
    
    for file_path in sys.argv[1:]:
        data = NVD.extract(file_path)
        if data is not None:
            # Save data to the database
            NVD.save2db(data, db_file, db_table)
        else:
            logger_vuln2db.error(f"Could not extract data from {file_path}")

if __name__ == "__main__":
    main()
