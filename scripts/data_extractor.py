import json
from requests_html import HTMLSession
from datetime import datetime
import os


# Helper function to get the absolute path of the data directory
def get_data_dir():
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


# Function to save data to a JSON file in the data directory
def save_to_json(data_list):
    ensure_data_dir_exists()
    file_path = os.path.join(get_data_dir(), "graph_data.json")
    try:
        with open(file_path, "w") as file:
            json.dump(data_list, file, indent=4)
    except Exception as e:
        log_error(f"An error occurred while saving data: {e}")


# Function to extract and save data
def extract_and_save():
    session = HTMLSession()
    r = session.get("https://esportsgava.deporsite.net/ocupacion-aforo")
    r.html.render(sleep=1)  # Give time for any JavaScript to execute

    graph_data = []
    selectors = [".col-1de3", ".col-2de3", ".col-3de3"]

    for selector in selectors:
        percentage_element = r.html.find(f"{selector} .percentage", first=True)
        facility_element = r.html.find(f"{selector} .nombre-recinto", first=True)

        if percentage_element and facility_element:
            percentage = percentage_element.text
            facility_name = facility_element.text
            detailed_data = facility_element.attrs["title"]
            current_and_max = detailed_data.split("|")[1].strip().split("/")

            data = {
                "facility": facility_name,
                "percentage": percentage,
                "current_occupancy": int(current_and_max[0]),
                "max_occupancy": int(current_and_max[1]),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            graph_data.append(data)

    if graph_data:
        save_to_json(graph_data)
        print("Data extracted and saved successfully.")
    else:
        log_error("No graph data could be extracted.")


# Function to run the data extraction process
def run_data_extraction():
    print("Running data extraction...")
    extract_and_save()


if __name__ == "__main__":
    run_data_extraction()
