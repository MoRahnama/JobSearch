"""
Automate NVD Processing Script
------------------------------

This script automates the processing of National Vulnerability Database (NVD) data. It retrieves the latest NVD JSON files, saves them in a specified downloads folder, and extracts relevant data to a database. It provides options for manual execution, scheduling, and reading the database.

Usage:
- Run the script manually to execute the data retrieval and processing.
- Schedule the script to run every hour automatically.
- Read the database to view the saved data.

Requirements:
- Python 3.x
- Required dependencies (install using pip): schedule

Folder Structure:
- nvd/
    - scripts/
        - Automate_nvd.py
    - lib/
        - NVD.py
        - Log.py

Modules:
- NVD: Module for NVD data retrieval, extraction, and database operations.
- Log: Module for setting up logging functionality.

Usage:
- Execute the script from the 'scripts' folder with the command: python Automate_nvd.py
- Follow the instructions on the prompt to choose the desired operation:
    - 'm': Run the script manually.
    - 'r': Read the database and view the saved data.
    - 'a': Schedule the script to run every hour automatically.

"""

import os
import schedule
import time
import sys

# Add the project root directory to the system path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# Now, perform the import
from lib import NVD
from lib import Log

# setup logger (Folder, File name, Logger Name)
logger_automate_nvd = Log.setup_log("log", "nvd", "automate_nvd")

def run_script():
    logger_automate_nvd.info("Running the script don't close the browser window that pops up...")

    # Specify the path to the downloads folder
    downloads_folder = 'download'

    # Run the download function to retrieve the latest NVD JSON files and save them in the downloads folder
    NVD.update(downloads_folder)

    # Add the database info here
    db_file = "nvd.db"
    db_table = "nvd_entries"

    # Get the list of files in the downloads folder
    file_list = os.listdir(downloads_folder)

    # Iterate over the files in the downloads folder
    years = ["2017.json", "2018.json", "2019.json", "2020.json", "2021.json"]

    for filename in file_list:
        file_path = os.path.join(downloads_folder, filename)
        for year in years:
            if file_path.endswith(year):
                if os.path.isfile(file_path):
                    # Run the extract function on the file
                    data = NVD.extract(file_path)
                    if data is not None:
                        # Save data to the database
                        NVD.save2db(data, db_file, db_table)
                    else:
                        logger_automate_nvd.error(f"Could not extract data from {file_path}")

def main():
    choice = input("Enter 'm' to run manually, 'r' to read the database file or 'a' to schedule it every hour: ")
    if choice.lower() == 'm':
        run_script()
    if choice.lower() == 'r':
        NVD.query_database("nvd.db", "nvd_entries")
    elif choice.lower() == 'a':
        # Schedule the script to run every hour
        schedule.every(1).hours.do(run_script)

        # Run the scheduler continuously
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
