# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY . /code/
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for static files
RUN mkdir -p /code/static

# Set permissions for the static files directory
RUN chown -R www-data:www-data /code/static

# Expose port 8000 to the outside world
EXPOSE 8000

# # Run Django app when the container launches
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
