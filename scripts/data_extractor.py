import json
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def extract_and_save():
    driver = None  # Define driver outside the try block
    try:
        # Set up Selenium WebDriver
        driver = webdriver.PhantomJS()
        driver.get('https://esportsgava.deporsite.net/ocupacion-aforo')

        # Wait for JavaScript to render
        time.sleep(5)

        # Extract data (Implement actual extraction logic)
        graph_data = {
            'graph1': {},
            'graph2': {},
            'graph3': {}
        }

        # Save data to a JSON file
        with open('graph_data.json', 'w') as file:
            json.dump(graph_data, file)

    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
        # Optionally, log the error to a file
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, log the error to a file
    finally:
        # Ensure the WebDriver is closed only if it was successfully created
        if driver is not None:
            driver.quit()

# Set up scheduler to run the extract_and_save function every 15 minutes
scheduler = BlockingScheduler()
scheduler.add_job(extract_and_save, 'interval', minutes=15)
scheduler.start()
