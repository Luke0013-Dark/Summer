# Use Debian as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    libxrender1 \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff6 \
    libwebp7 \
    libx11-6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webhook_app.py .

# Expose port (Railway will set PORT env var, FastHTML default is 5000)
EXPOSE $PORT

# Run the application
CMD ["python", "webhook_app.py"]