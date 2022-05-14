
FROM python:3

WORKDIR /app

COPY ./requirements.txt .

RUN ["pip3", "install", "-r", "requirements.txt"]

# add app
COPY . .

EXPOSE 5000

CMD [ "python3", "server.py"]