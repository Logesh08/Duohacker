FROM python:3.11-slim

WORKDIR /srv


RUN apt-get update \
    && apt-get install -y zip unzip curl gnupg wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip


# Install chrome broswer
RUN curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable jq

# Install chromedriver
RUN driver_json_url="https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" && \
    stable_version=$(curl -s $driver_json_url | jq -r '.channels.Stable.version') && \
    wget -N "https://storage.googleapis.com/chrome-for-testing-public/$stable_version/linux64/chromedriver-linux64.zip" -P ~/
#RUN wget -N "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$(google-chrome-stable --version | awk '{print $3}')/linux64/chromedriver-linux64.zip" -P ~/
RUN unzip ~/chromedriver-linux64.zip -d ~/
RUN rm ~/chromedriver-linux64.zip
RUN mv -f ~/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

COPY ./requirements.txt .
RUN pip install -r requirements.txt
ADD . /srv

EXPOSE 9222

CMD ["python", "-u", "app.py"]
