FROM python:3-alpine3.19 as base
RUN apk update

RUN apk add --no-cache mariadb-dev gcc musl-dev mariadb-connector-c-dev python3-dev 

WORKDIR /src/piiops

RUN pip3 install --upgrade pip
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

FROM base

COPY . .

CMD [ "python", "./pii_frontend.py" ]

