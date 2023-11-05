from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
import json
import time

def extract_and_save():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(executable_path='C:\\Users\\TeH_h\\OneDrive\\Documentos\\Python Scripts\\chrome-win64\\chromedriver.exe')
    driver.get('https://esportsgava.deporsite.net/ocupacion-aforo')

    # Wait for JavaScript to render
    time.sleep(5)  # Adjust this wait time as needed

    # Extract graph data (This is a placeholder, you'll need to implement the actual extraction)
    graph_data = {
        'graph1': {},
        'graph2': {},
        'graph3': {}
    }

    # Save data to a JSON file
    with open('graph_data.json', 'w') as file:
        json.dump(graph_data, file)

    # Close the WebDriver
    driver.quit()

# Set up scheduler to run the extract_and_save function every 15 minutes
scheduler = BlockingScheduler()
scheduler.add_job(extract_and_save, 'interval', minutes=15)
scheduler.start()
