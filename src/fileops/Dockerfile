FROM python:3-alpine3.19 as base
RUN apk update
#RUN apt -y install gcc
#RUN apt-get install -y libmariadb-dev

RUN apk add --no-cache mariadb-dev gcc musl-dev mariadb-connector-c-dev python3-dev 

WORKDIR /src/fileops

RUN pip3 install --upgrade pip
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./fileops.py" ]