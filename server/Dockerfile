'''
University of Melbourne
COMP90024 Cluster and Cloud Computing
2022 Semester 1 Assignment 2

Team 58:
- (Sam)    Bin Zhang,    895427 @ Melbourne
- (Joe)    Tianhuan Lu,  894310 @ Melbourne
- (Leo)    Yicong Li,   1307323 @ Melbourne
- (Peter)  Weiran Zou,  1309198 @ Melbourne
- (Thomas) Chenhao Gu,  1147534 @ Melbourne
'''
FROM python:3

WORKDIR /app

COPY ./requirements.txt .

RUN ["pip3", "install", "-r", "requirements.txt"]

# add app
COPY . .

EXPOSE 5000

CMD [ "python3", "server.py"]