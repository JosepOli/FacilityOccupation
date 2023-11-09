import json
from requests_html import HTMLSession
from datetime import datetime


# Function to extract and save data
def extract_and_save():
    session = HTMLSession()
    url = "https://esportsgava.deporsite.net/ocupacion-aforo"
    graph_data = []

    try:
        r = session.get(url)
        r.html.render(sleep=10)  # Give time for any JavaScript to execute

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

        if not graph_data:
            raise ValueError("No data found in the extracted content.")

        # Save the extracted data to a JSON file
        with open("graph_data.json", "w") as json_file:
            json.dump(graph_data, json_file, indent=4)

    except Exception as e:
        # Log the HTML content to a file for inspection
        with open("page_content.html", "w") as file:
            file.write(r.html.html)
        print(f"An error occurred: {e}")
        print(f"The HTML content was saved to page_content.html for inspection.")
        # Optionally re-raise the exception to make the script exit with an error
        raise


if __name__ == "__main__":
    extract_and_save()
