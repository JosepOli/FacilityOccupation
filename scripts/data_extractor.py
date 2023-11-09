import json
from requests_html import HTMLSession
from datetime import datetime


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
        with open("graph_data.json", "w") as file:
            json.dump(graph_data, file, indent=4)
        print("Data extracted and saved successfully.")
    else:
        print("No graph data could be extracted.")


if __name__ == "__main__":
    extract_and_save()
