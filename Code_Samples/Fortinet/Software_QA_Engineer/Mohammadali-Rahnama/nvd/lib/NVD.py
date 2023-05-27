import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import requests
import zipfile
import filecmp

from lib import Log

# setup logger (Folder, File name, Logger Name)
logger_save2db = Log.setup_log("log", "nvd", "save2db")
logger_extract = Log.setup_log("log", "nvd", "extract")
logger_download = Log.setup_log("log", "nvd", "download")

def extract(json_file_path):
    """
    Reads a JSON file at json_file_path and converts its contents into a pandas DataFrame.

    Args:
        json_file_path (str): The path to the NVD JSON file to be parsed.
    
    Returns:
        pandas.DataFrame: The DataFrame containing the converted data.
    """
    logger_extract.info(f"Processing file: {json_file_path}")
    try:
        data_frame = pd.read_json(json_file_path)
        logger_extract.info("File processed successfully")
        return data_frame
    except FileNotFoundError as e:
        logger_extract.error(f"File not found: {json_file_path}")
    except ValueError as e:
        logger_extract.error(f"Error reading JSON data from {json_file_path}: {str(e)}")
    except pd.errors.JSONDecodeError as e:
        logger_extract.error(f"Error decoding JSON data from {json_file_path}: {str(e)}")
    return None


def save2db(data, db_file, db_table):

    """
    Saves the extracted NVD data to a database table.

    Args:
        data (pandas.DataFrame): The extracted NVD data as a DataFrame.
        db_file (str): The path to the database file.
        db_table (str): The name of the database table to save the data to.
    """

    logger_save2db.info("Connecting to database...")
    # Create a connection to the database using SQLAlchemy
    engine = create_engine(f'sqlite:///{db_file}')
    
    records = []

    for i in range(len(data)):
        id = data.iloc[i]['CVE_Items']['cve']['CVE_data_meta']['ID']
        base_severity = None
        if 'baseMetricV3' in data.iloc[i]['CVE_Items']['impact']:
            base_severity = data.iloc[i]['CVE_Items']['impact']['baseMetricV3']['cvssV3']['baseSeverity']
        elif 'baseMetricV2' in data.iloc[i]['CVE_Items']['impact']:
            base_severity = data.iloc[i]['CVE_Items']['impact']['baseMetricV2']['cvssV2']['severity']
        published_date = data.iloc[i]['CVE_Items']['publishedDate']
        last_modified_date = data.iloc[i]['CVE_Items']['lastModifiedDate']
        
        # Add the data to the records list
        records.append([id, base_severity, published_date, last_modified_date])

    # Convert the records list to a DataFrame
    data_to_insert = pd.DataFrame(records, columns=['ID', 'baseSeverity', 'publishedDate', 'lastModifiedDate'])

    # Use pandas to_sql to insert the DataFrame into the database
    data_to_insert.to_sql(db_table, con=engine, index=False, if_exists='replace')

    logger_save2db.info("Data saved to database successfully.")

def update(downloads_folder):

    """
    Updates the NVD data by downloading the latest JSON files and extracting them to the specified folder.

    Args:
        downloads_folder (str): The path to the folder where the downloaded files will be saved.
    """

    # Path to your web driver executable
    webdriver_path = 'path_to_web_driver_executable'

    # Start the Selenium webdriver
    driver = webdriver.Chrome(webdriver_path)

    # Navigate to the web page
    driver.get('https://nvd.nist.gov/vuln/data-feeds')

    try:
        # Find the div element with id "divJSONFeeds"
        div_element = driver.find_element(By.ID, 'divJSONFeeds')

        # Find the table element within the div element
        table = div_element.find_element(By.TAG_NAME, 'table')

        # Find all the rows in the table body
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        # Create a downloads folder if it doesn't exist
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)

         # Check if an existing updated.txt file exists
        existing_file_path = os.path.join(downloads_folder, 'updated.txt')
        if not os.path.exists(existing_file_path):
            update_file_path = os.path.join(downloads_folder, 'updated.txt')
             # Open the text file for writing in the downloads folder
            with open(update_file_path, 'w') as file:
                # Iterate over the rows and extract the Updated values
                for row in rows:
                    updated = row.find_element(By.XPATH, './td[2]').text
                    file.write(f'{updated}\n')

        # if an existing updated.txt file does exists
        elif os.path.exists(existing_file_path):
            # Create a temp text file
            updated_file_path = os.path.join(downloads_folder, 'temp_updated.txt')
            with open(updated_file_path, 'w') as file:
                # Iterate over the rows and extract the Updated values
                for row in rows:
                    updated = row.find_element(By.XPATH, './td[2]').text
                    file.write(f'{updated}\n')
            # Compare the existing file with the new file
            if filecmp.cmp(existing_file_path, updated_file_path):
                logger_download.info("No new updates found. Skipping download.")
                # Close the browser
                driver.quit()
                return
            else:
                # the files don't match we have save the temp as the original updated.txt file
                os.remove(existing_file_path)
                os.rename(updated_file_path, os.path.join(downloads_folder, 'updated.txt'))

        # Find all the links within the table
        links = table.find_elements(By.TAG_NAME, 'a')

        # Iterate over the links and download the ZIP files
        for link in links:
            url = link.get_attribute('href')
            if url.endswith('.zip'):
                # Download the ZIP file
                response = requests.get(url)
                zip_filename = os.path.join(downloads_folder, os.path.basename(url))
                with open(zip_filename, 'wb') as zip_file:
                    zip_file.write(response.content)
                
                # Extract the contents of the ZIP file to the downloads folder
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall(downloads_folder)
                
                logger_download.info(f"Extracted: {url}")
                
                # Delete the ZIP file
                os.remove(zip_filename)
        
        logger_download.info("File processing completed successfully.")

    except Exception as e:
        logger_download.error("An error occurred during file processing.", exc_info=True)

    finally:
        # Close the browser
        driver.quit()

def query_database(db_file, db_table):
    """
    Retrieves data from the specified database table and prints it.

    Args:
        db_file (str): The path to the database file.
        db_table (str): The name of the database table to query.
    """
    # Create engine that will interact with the database
    engine = create_engine(f'sqlite:///{db_file}')

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # Create a session
    session = Session()

    try:
        # Make a query to the database
        rows = session.execute(text(f'SELECT * FROM {db_table}'))

        # Fetch and print all rows from the query
        for row in rows:
            print(row)
    except Exception as e:
        print(f"An error occurred during the database query: {e}")
    finally:
        # Close the session
        session.close()

