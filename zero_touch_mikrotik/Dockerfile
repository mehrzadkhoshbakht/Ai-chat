# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install system dependencies required for libraries like moviepy and pydub
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# We run bootstrap.py's install_dependencies function to ensure all packages are installed
RUN python bootstrap.py

# The command to run when the container starts
# This will start a Celery worker to listen for tasks
CMD ["celery", "-A", "orchestrator", "worker", "--loglevel=info"]
