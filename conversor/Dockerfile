FROM python:3.8-slim-buster

WORKDIR /python-docker

ADD conversion.py /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

## following 3 lines are for installing ffmepg
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY . .

CMD ["python", "./conversion.py"]