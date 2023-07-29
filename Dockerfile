FROM python:3




RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get install zip -y
RUN apt-get install unzip -y


RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxi6 \
    libxext6 \
    libxtst6 \
    libnss3 \
    libcups2 \
    libxss1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libgtk-3-0


# Install chromedriver
RUN wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.102/linux64/chromedriver-linux64.zip -P ~/ 
RUN unzip ~/chromedriver-linux64.zip -d ~/
RUN rm ~/chromedriver-linux64.zip
RUN mv -f ~/chromedriver-linux64 /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver


# Install chrome broswer
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable
# Run search_and_like.py when the container launches

ENV LOG_LEVEL=INFO

CMD ["python3", "search_and_like.py", "--article", "https://www.pudelek.pl/kinga-rusin-komentuje-tragiczny-pozar-na-rodos-ewakuowano-wszystkich-mieszkancow-miejscowosci-sasiadujacej-z-nasza-wioska-6923733386107872a?fbclid", "--comment", "A ja uważam, ze Kinga takimi postami się zwyczajnie promuje. To jest ludzka tragedia, a dla pani pretekst żeby wrzucić swoje zdjęcie. Taki jest zreszta cały instagram. Niewazne jak poważny post, każdy obudowany jest selfikiem. Inna sprawa, że nagle każdy celebryta mieszka w Grecji, zna każda uliczkę i robi zakupy w lokalnych sklepach. Grecja jest popularnym kierunkiem, nie tylko wy tam jeździcie, drodzy celebryci ;)", "--like_dislike", "dislike"]

