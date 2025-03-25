# Use official Python image
FROM python:3.10

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ultralytics YOLOv8
RUN pip install ultralytics

# Copy AI job script
COPY . .

# Default command (change if needed)
CMD ["python", "process.py"]