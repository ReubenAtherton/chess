FROM python:3.9-slim

WORKDIR /app

# Set Python path to include the src directory
ENV PYTHONPATH=/app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.main.api:app"] 