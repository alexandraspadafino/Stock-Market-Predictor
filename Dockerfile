# Use the official Node.js image as a base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Ensure pip is isntalled and up to date 
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt first to install dependencies
COPY requirements.txt .

# Copy the rest of your app’s source code
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code 
COPY . .

# Expose the port that your app runs on (e.g., 3000 for React)
EXPOSE 8502

# Command to run your app (change this to whatever command you use)
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]