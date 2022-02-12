# syntax=docker/dockerfile:1

FROM python:3-slim-buster

# Copy the application code
ADD flask-app /opt/flask-app
WORKDIR /opt/flask-app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY flask-app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "./app.py"]
