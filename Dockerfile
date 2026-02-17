# Use slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 9999

# Start application
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "9999"]
