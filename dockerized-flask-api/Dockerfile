# Use official Python image as base
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /docker

# Install system dependencies (if needed)
# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y gcc python3-dev

# Copy requirements first to leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port that Flask runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "main.py"]