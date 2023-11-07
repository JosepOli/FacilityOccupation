FROM arm32v7/python:3.8-slim

WORKDIR /usr/src/app

# Install system dependencies for lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libffi-dev \
    libssl-dev \
    gcc \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
 && pip install --upgrade pip

# Install Python dependencies
RUN pip install --verbose --no-cache-dir Flask requests-html

# Remove unnecessary system packages and clear apt cache to reduce image size
RUN apt-get purge -y --auto-remove gcc libffi-dev libssl-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy the application source code to the container
COPY . .

# Command to run the application
CMD ["python", "./app.py"]
