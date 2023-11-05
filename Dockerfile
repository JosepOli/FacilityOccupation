FROM python:3.9.2
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y \
    netcat \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./data_extractor.py"]

