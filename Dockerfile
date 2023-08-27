FROM ubuntu:20.04

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PROJ_DIR=/usr

RUN apt update && apt upgrade -y

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.7
RUN apt-get install -y apt-utils python3-pip libglib2.0-0 python3-wheel python3-setuptools python3-pip python3-opengl python3.7-distutils python3-apt libsm6 libxext6 libxrender-dev

COPY . /app/
RUN python3.7 -m pip install -r requirements.txt

EXPOSE 9100

CMD ["python3.7", "/app/server.py"]