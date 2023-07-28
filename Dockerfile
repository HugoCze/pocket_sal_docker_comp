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


# Step 2: Install Chrome
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Step 3: Download Chromedriver
# Make sure to replace 'x.x.x.x' with the appropriate version of Chromedriver that matches your installed Chrome version.
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/x.x.x.x/chromedriver_linux64.zip

# Step 4: Unzip and move Chromedriver to /usr/local/bin
RUN apt-get install -y unzip
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Step 5: Set executable permissions for Chromedriver
RUN chmod +x /usr/local/bin/chromedriver

# Step 6: Clean up
RUN rm /tmp/chromedriver.zip

# Copy the current directory contents into the container at /app
COPY src/ ./

# Install pip and any needed packages specified in requirements.txt
RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends python3-pip && \
    sudo pip3 install selenium argparse

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