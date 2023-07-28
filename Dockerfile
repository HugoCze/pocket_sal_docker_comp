# Use the Selenium/standalone-chrome image as the base
FROM selenium/standalone-chrome:latest

# Set the working directory inside the container
WORKDIR /app

# Install Python and any additional dependencies needed for your Selenium project
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optionally, set a specific Python version by installing it manually
# RUN apt-get install -y python3.9

# Copy your Selenium project into the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set any environment variables needed for your Selenium project
# ENV VARIABLE_NAME value

# Run your Python script using the Selenium application
CMD ["python3", "your_selenium_script.py"]
