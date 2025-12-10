# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy requirements files first (for better Docker layer caching)
COPY requirements.txt ./
COPY pyproject.toml ./

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt (if not empty)
RUN if [ -s requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Install project dependencies from pyproject.toml
RUN pip install --no-cache-dir -e .

# Copy the rest of the application code
COPY . .

# Expose any ports if needed (not required for this MCP server)
EXPOSE 8011

# Set environment variables for the email service
# These should be provided at runtime
ENV SENDER_EMAIL_ID=""
ENV TENANT_ID=""
ENV CLIENT_ID=""
ENV CLIENT_SECRET=""

# Run the main application
CMD ["python", "main.py"]