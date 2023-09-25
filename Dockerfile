FROM python:3.10-slim-buster
WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /opt/app
CMD ["sh", "-c", "python manage.py makemigration && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
