FROM python:3.8
COPY . /usr/src/MenuTelegramBot
WORKDIR /usr/src/MenuTelegramBot/

ENV TZ=Europe/Moscow
RUN pip3 install --no-cache-dir -r requirements.txt
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD /wait && python3 app.py