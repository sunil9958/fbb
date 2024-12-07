# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install aria2 only
RUN apt-get update && apt-get install -y aria2 && apt-get clean

# Copy project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the service using start.sh
CMD ["bash", "start.sh"]
