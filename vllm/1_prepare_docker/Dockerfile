# Use the base image specified in your YAML
FROM vllm/vllm-openai:latest

# Set the working directory
WORKDIR /app

# Copy the local model directory into the Docker image
COPY /path/to/local/model /models/meta-llama

# Ensure necessary environment variables are set
ENV TRANSFORMERS_CACHE=/.cache
ENV SHM_SIZE=1g

# Install any additional dependencies if required
# RUN pip install <additional-dependencies>

# Expose the port
EXPOSE 8000
