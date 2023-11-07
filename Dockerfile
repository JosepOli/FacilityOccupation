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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies one by one
RUN pip install --verbose --no-cache-dir Flask==1.1.2
RUN pip install --verbose --no-cache-dir requests-html==0.10.0
RUN pip install --verbose --no-cache-dir aiohttp==3.7.4.post0

# Copy the application source code to the container
COPY . .

# Command to run the application
CMD ["python", "./app.py"]
