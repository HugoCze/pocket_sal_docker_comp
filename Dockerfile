# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster
FROM selenium/standalone-chrome:latest

# Create a new user and switch to that user
USER root
RUN groupadd -r myuser && useradd -r -g myuser myuser
USER myuser

# Set the working directory in the container to /app
WORKDIR /pocketSAL

# Install required dependencies
RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends git curl && \
    sudo rm -rf /var/lib/apt/lists/*

# Download and install ChromeDriver
RUN CHROMEDRIVER_VERSION=2.41 && \
    curl -O -L https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    chmod +x chromedriver && \
    sudo mv chromedriver /usr/bin/chromedriver

# Copy the current directory contents into the container at /app
COPY src/ ./

# Install pip and any needed packages specified in requirements.txt
RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends python3-pip && \
    sudo pip3 install --no-cache-dir -r requirements.txt

RUN sudo pip3 install --upgrade selenium

# Make sure the Python executable path is set in the environment variable
ENV PATH="/usr/local/bin:${PATH}"

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your script when the container launches

CMD ["python3", "search_and_like.py", "--article", "https://www.pudelek.pl/sprawa-joanna-z-krakowa-kinga-rusin-miazdzy-pis-i-polska-policje-kazali-jej-sie-rozebrac-do-naga-choc-krwawila-6921586600442848a?fbclid=IwAR2XwfbyjdWMuq5ALuZZaQCpM0zIGyUh4wkvQPOEuu8P_-dQqNw0aZaVZGc", "--comment", "Masakraaaa biedna kobieta", "--like_dislike", "like"]


# CMD ["python3", "search_and_like.py", "--article", "https://www.pudelek.pl/sprawa-joanna-z-krakowa-kinga-rusin-miazdzy-pis-i-polska-policje-kazali-jej-sie-rozebrac-do-naga-choc-krwawila-6921586600442848a?fbclid=IwAR2XwfbyjdWMuq5ALuZZaQCpM0zIGyUh4wkvQPOEuu8P_-dQqNw0aZaVZGc", "--comment", "Ma więcej niż rację. Dramat co się u na wyprawia.", "--like_dislike", "like"]

# CMD ["python", '.\src\search_and_like.py --article "https://www.pudelek.pl/sprawa-joanny-z-krakowa-kinga-rusin-miazdzy-pis-i-polska-policje-kazali-jej-sie-rozebrac-do-naga-choc-krwawila-6921586600442848a?fbclid=IwAR2XwfbyjdWMuq5ALuZZaQCpM0zIGyUh4wkvQPOEuu8P_-dQqNw0aZaVZGc" --comment "Ma więcej niż rację. Dramat co się u na wyprawia." --like_dislike "like"']
# python .\src\search_and_like.py --article "https://www.pudelek.pl/sprawa-joanny-z-krakowa-kinga-rusin-miazdzy-pis-i-polska-policje-kazali-jej-sie-rozebrac-do-naga-choc-krwawila-6921586600442848a?fbclid=IwAR2XwfbyjdWMuq5ALuZZaQCpM0zIGyUh4wkvQPOEuu8P_-dQqNw0aZaVZGc" --comment "Ma więcej niż rację. Dramat co się u na wyprawia." --like_dislike "like"