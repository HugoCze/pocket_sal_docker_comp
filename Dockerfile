# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Download and install Chrome WebDriver
ENV CHROME_DRIVER_VERSION 94.0.4606.41
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver

# Copy your Selenium project into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set any environment variables needed for your Selenium project
# ENV VARIABLE_NAME value

# Run your Python script using the Selenium application
CMD ["python3", "search_and_like.py", "--article", "https://www.pudelek.pl/kinga-rusin-komentuje-tragiczny-pozar-na-rodos-ewakuowano-wszystkich-mieszkancow-miejscowosci-sasiadujacej-z-nasza-wioska-6923733386107872a?fbclid=IwAR0eb8JgpF4vPFCyvRNT_5kqnhePmDNu1EHBWo_l0fd7fyQR_TFwZNDklJc", "--comment", "A ja uważam, ze Kinga takimi postami się zwyczajnie promuje. To jest ludzka tragedia, a dla pani pretekst żeby wrzucić swoje zdjęcie. Taki jest zreszta cały instagram. Niewazne jak poważny post, każdy obudowany jest selfikiem. Inna sprawa, że nagle każdy celebryta mieszka w Grecji, zna każda uliczkę i robi zakupy w lokalnych sklepach. Grecja jest popularnym kierunkiem, nie tylko wy tam jeździcie, drodzy celebryci ;)", "--like_dislike", "dislike"]
