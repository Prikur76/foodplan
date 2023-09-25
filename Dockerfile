FROM python:3.10-slim-buster
WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /opt/app 
copy entrypoint.sh /entrypoint.sh
entrypoint /entrypoint.sh
