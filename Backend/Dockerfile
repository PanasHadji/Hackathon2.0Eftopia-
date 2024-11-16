# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /Backend

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential

# Install torch separately first
RUN pip install --no-cache-dir torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
RUN pip install numpy==1.22.0 scikit-learn==1.0.2

# Copy the requirements.txt into the container
COPY requirements.txt /Backend/requirements.txt

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /Backend

# Expose the application port
EXPOSE 5001

# Command to run the application using uvicorn
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "5001"]
