# Step 1: Use an official Python runtime as a base image
FROM python:3.12-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port FastAPI will run on
EXPOSE 8000

# Step 6: Set environment variables (Optional, if not using .env)
# ENV COMFYUI_SERVER_ADDRESS=192.168.1.10:8188
# ENV OLLAMA_SERVER_ADDRESS=192.168.1.10:11436

# Step 7: Run FastAPI using Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]