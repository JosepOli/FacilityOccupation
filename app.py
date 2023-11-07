from flask import Flask, jsonify, render_template, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# Helper function to get the absolute path of the data directory
def get_data_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    
    # Convert the start and end dates from string to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    data_dir = get_data_dir()
    file_path = os.path.join(data_dir, 'graph_data.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Filter data by date range if start and end dates are provided
            if start_date and end_date:
                data = [entry for entry in data if start_date <= datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S') <= end_date]
            return jsonify(data)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
