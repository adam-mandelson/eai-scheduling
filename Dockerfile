# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /eai_planday

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m", "get_reports", "2022 02"]
