FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3 python-pip python-dev build-essential python3-distutils python3-dev && \
    apt install -y libmysqlclient-dev

RUN echo "LC_ALL=C.UTF-8" >> /etc/environment 
RUN echo "LANG=C.UTF-8" >> /etc/environment 

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /app

WORKDIR /app

RUN pip install pipenv 

RUN pipenv install

CMD [ "pipenv", "run", "flask", "run", "--host=0.0.0.0" ]
