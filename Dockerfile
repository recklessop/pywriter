FROM python:3

WORKDIR /usr/src

RUN git clone https://github.com/recklessop/pywriter.git

WORKDIR /usr/src/pywriter

RUN apt-get update; apt-get upgrade -t; apt-get install build-essential unixodbc-dev -y

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./pywriter.py" ]
