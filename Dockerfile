FROM python:3

WORKDIR /usr/src

RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EB3E94ADBE1229CF
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y

RUN apt-get update; apt-get upgrade -y; apt-get install build-essential unixodbc-dev libgssapi-krb5-2 -y

RUN git clone https://github.com/recklessop/pywriter.git

WORKDIR /usr/src/pywriter

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./pywriter.py" ]
