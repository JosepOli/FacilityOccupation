# Using an ARM architecture Python base image compatible with Raspberry Pi
FROM arm32v7/python:3.9-slim

# Setting the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code to the container
COPY . .

# Command to run the application
CMD ["python", "./app.py"]
