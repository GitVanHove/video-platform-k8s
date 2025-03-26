# Use official Python image
FROM python:3.10

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt


# Copy AI job script
COPY . . 

# Expose the Flask API port
EXPOSE 5001

# Default command (change if needed)
CMD ["python", "process_video.py"]