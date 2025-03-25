# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose Flask's default port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]