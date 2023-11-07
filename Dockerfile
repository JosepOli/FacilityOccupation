# Using an ARM architecture Python base image compatible with Raspberry Pi
FROM arm32v7/python:3.6-slim

# Setting the working directory in the container
WORKDIR /usr/src/app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libffi-dev \
    libssl-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --verbose --no-cache-dir -r requirements.txt

# Copy the application source code to the container
COPY . .

# Command to run the application
CMD ["python", "./app.py"]
