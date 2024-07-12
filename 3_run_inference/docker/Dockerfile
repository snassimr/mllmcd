# Use the existing image as the base image
FROM mllmcd:latest

# Set the working directory in the container
WORKDIR /server

COPY model/ model/

# Copy your FastAPI application code into the container
COPY fastapi_server.py .
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Command to run the FastAPI server
# CMD ["python3", "fastapi_server.py", "model_dir", "model", "--host", "0.0.0.0", "--port", "8000"]

