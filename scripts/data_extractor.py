import json
import asyncio
from pyppeteer import launch
from datetime import datetime
import os


# Helper function to get the absolute path of the data directory
def get_data_dir():
    # This will get one directory up from the current script's directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data")


# Ensure that the data directory exists
def ensure_data_dir_exists():
    data_dir = get_data_dir()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


# Function to log errors to a file in the data directory
def log_error(error_message):
    ensure_data_dir_exists()
    error_log_path = os.path.join(get_data_dir(), "error_log.txt")
    with open(error_log_path, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {error_message}\n")


# Function to append a list of data to a JSON file in the data directory
def append_to_json(data_list):
    ensure_data_dir_exists()
    file_path = os.path.join(get_data_dir(), "graph_data.json")
    try:
        # Load existing data if the file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                file_data = json.load(file)
        else:
            file_data = []

        # Append new data to the existing data
        file_data.extend(data_list)  # Use extend() to concatenate lists

        # Write the updated data to the file
        with open(file_path, "w") as file:
            json.dump(file_data, file, indent=4)
    except Exception as e:
        log_error(f"An error occurred while appending data: {e}")


# Function to extract graph data
async def extract_graph_data(page, selector):
    try:
        # Wait for the SVG element that contains the percentage to be visible and get its text content
        percentage_element = await page.waitForSelector(
            f"{selector} .percentage", {"visible": True}
        )
        percentage = await page.evaluate(
            "(element) => element.textContent", percentage_element
        )

        # Wait for the DIV element that contains the facility name, current, and max occupancy to be visible and get its text content
        facility_element = await page.waitForSelector(
            f"{selector} .nombre-recinto", {"visible": True}
        )
        facility_name = await page.evaluate(
            "(element) => element.textContent", facility_element
        )

        # Wait for the same DIV element to get its title attribute for current and max occupancy
        detailed_data = await page.evaluate(
            '(element) => element.getAttribute("title")', facility_element
        )
        # Parse the detailed data to extract current and max occupancy
        current_and_max = detailed_data.split("|")[1].strip().split("/")

        data = {
            "facility": facility_name,
            "percentage": percentage,
            "current_occupancy": int(current_and_max[0]),
            "max_occupancy": int(current_and_max[1]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return data
    except Exception as e:
        log_error(f"An error occurred while extracting graph data: {e}")
        return None


# Function to extract and save data
async def extract_and_save():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(
        "https://esportsgava.deporsite.net/ocupacion-aforo",
        {"waitUntil": "networkidle0"},
    )

    selectors = [".col-1de3", ".col-2de3", ".col-3de3"]
    graph_data = []

    for selector in selectors:
        data = await extract_graph_data(page, selector)
        if data:
            graph_data.append(data)

    await browser.close()

    if graph_data:
        append_to_json(graph_data)  # Changed this line to use the new function directly
        print("Data extracted and saved successfully.")
    else:
        log_error("No graph data could be extracted.")


# Function to manually test the script
def manual_test():
    print("Starting test of the script...")
    asyncio.get_event_loop().run_until_complete(extract_and_save())


if __name__ == "__main__":
    manual_test()
