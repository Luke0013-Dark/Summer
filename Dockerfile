# Use Debian as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install only the most essential packages for OCR
RUN apt-get update && apt-get install -y \
    libxrender1 \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff6 \
    libwebp7 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port (Railway will set PORT env var)
EXPOSE $PORT

# Run the application
CMD ["python", "app.py"]