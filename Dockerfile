FROM python:3.10-slim-buster
WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /opt/app 
CMD [ "python", "./manage.py", "makemigrations"]
CMD [ "python", "./manage.py", "migrate"]
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
