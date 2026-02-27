# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 5005

# Set Flask app
ENV FLASK_APP=app.py

# Start Flask on all interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=5005"]
