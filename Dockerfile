FROM python:3.10-slim-buster
WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /opt/app
RUN python manage.py migrate
CMD [ "python", "./manage.py", "runserver"]
