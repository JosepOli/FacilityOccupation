from collections import defaultdict
from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)


# Helper function to get the absolute path of the data directory
def get_data_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data")


def get_average_occupancy(data, start_time, end_time):
    # Aggregate data by hour and calculate average occupancy
    hourly_data = defaultdict(list)
    for entry in data:
        timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        if start_time <= timestamp.time() <= end_time:
            hourly_data[timestamp.hour].append(entry["current_occupancy"])
    hourly_averages = {
        hour: sum(values) / len(values) for hour, values in hourly_data.items()
    }
    return hourly_averages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    time_frame = request.args.get("time_frame")
    data_dir = get_data_dir()
    file_path = os.path.join(data_dir, "graph_data.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        # Filter data based on time_frame
        if time_frame:
            now = datetime.now()
            if time_frame == "last-week":
                start_date = now - timedelta(days=now.weekday(), weeks=1)
                end_date = start_date + timedelta(days=6)
            elif time_frame == "last-month":
                first_day_last_month = (now.replace(day=1) - timedelta(days=1)).replace(
                    day=1
                )
                last_day_last_month = now.replace(day=1) - timedelta(days=1)
                start_date = first_day_last_month
                end_date = last_day_last_month
            # Filter the data for the specified date range
            data = [
                entry
                for entry in data
                if start_date
                <= datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").date()
                <= end_date
            ]

        return jsonify(data)
    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
