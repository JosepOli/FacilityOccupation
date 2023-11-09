FROM arm32v7/python:3.8-alpine

WORKDIR /usr/src/app

# Install Python dependencies
RUN pip install --no-cache-dir Flask

# Copy the application source code to the container
COPY . .

# Command to run the application
CMD ["python", "./app.py"]
