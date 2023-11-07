import json
import asyncio
from pyppeteer import launch
from datetime import datetime
import os

# Ensure cross-platform compatibility for file paths
def ensure_file_path(file_name):
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(project_root, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, file_name)

# Function to log errors to a file
def log_error(error_message):
    error_log_path = ensure_file_path('error_log.txt')
    with open(error_log_path, 'a') as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{timestamp} - {error_message}\n")

# Function to append a list of data to a JSON file
def append_to_json(file_path, data_list):
    try:
        # Load existing data if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                # Ensure the loaded data is a list, if not initialize an empty list
                file_data = json.load(file)
                if not isinstance(file_data, list):
                    file_data = []
        else:
            file_data = []

        # Append new data to the existing data
        file_data += data_list  # Use += to concatenate list
        
        # Write the updated data to the file
        with open(file_path, 'w') as file:
            json.dump(file_data, file, indent=4)
    except Exception as e:
        log_error(f"An error occurred while appending data: {e}")

# Function to extract graph data
async def extract_graph_data(page, selector):
    try:
        # Wait for the SVG element that contains the percentage to be visible and get its text content
        percentage_element = await page.waitForSelector(f'{selector} .percentage', {'visible': True})
        percentage = await page.evaluate('(element) => element.textContent', percentage_element)

        # Wait for the DIV element that contains the facility name, current, and max occupancy to be visible and get its text content
        facility_element = await page.waitForSelector(f'{selector} .nombre-recinto', {'visible': True})
        facility_name = await page.evaluate('(element) => element.textContent', facility_element)

        # Wait for the same DIV element to get its title attribute for current and max occupancy
        detailed_data = await page.evaluate('(element) => element.getAttribute("title")', facility_element)
        # Parse the detailed data to extract current and max occupancy
        current_and_max = detailed_data.split('|')[1].strip().split('/')

        data = {
            'facility': facility_name,
            'percentage': percentage,
            'current_occupancy': int(current_and_max[0]),
            'max_occupancy': int(current_and_max[1]),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return data
    except Exception as e:
        log_error(f"An error occurred while extracting graph data: {e}")
        return None


# Function to extract and save data
async def extract_and_save():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://esportsgava.deporsite.net/ocupacion-aforo', {'waitUntil': 'networkidle0'})

    selectors = ['.col-1de3', '.col-2de3', '.col-3de3']
    graph_data = []

    for selector in selectors:
        data = await extract_graph_data(page, selector)
        if data:
            graph_data.append(data)

    await browser.close()

    if graph_data:
        append_to_json(ensure_file_path('graph_data.json'), graph_data)
        print("Data extracted and saved successfully.")
    else:
        log_error("No graph data could be extracted.")

# Function to manually test the script
def manual_test():
    print("Starting manual test of the script...")
    asyncio.get_event_loop().run_until_complete(extract_and_save())

if __name__ == "__main__":
    manual_test()
