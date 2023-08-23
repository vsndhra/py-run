# Use a base image with Python
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements & install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of the app's files
COPY . .

# Expose port which Gunicorn will use
EXPOSE 5000

# Run Gunicorn with the Flask app
CMD ["gunicorn", "-w", "4", "app:app"]
