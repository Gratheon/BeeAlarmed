FROM ubuntu:20.04

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PROJ_DIR=/usr

RUN apt-get update && apt-get upgrade -y
#python3.7-dev

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.7

RUN apt-get install -y python3-pip libglib2.0-0

# Install dependencies
# RUN apt-get install -y git wget lsb-release software-properties-common

# Install build-essential
# RUN apt-get install -y build-essential curl

# Install systemd
# RUN apt-get install -y systemd systemd-sysv

# Install python libs
#RUN apt-get install -y python3-wheel python3-setuptools python3-pip
RUN apt-get install -y python3-wheel
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-pip
# RUN apt-get install -y python3-paho-mqtt python3-logzero python3-astor
RUN apt-get install -y python3-opengl

#python3-six python3-grpcio
# RUN apt-get install -y python3-keras-applications python3-keras-preprocessing
# RUN apt-get install -y python3-protobuf python3-termcolor python3-numpy
# RUN apt-get install -y pkg-config python3-h5py libhdf5-dev
# RUN python3.7 -m pip install --upgrade pip setuptools wheel
RUN apt-get install -y python3.7-distutils python3-apt
#RUN dpkg -i --force-overwrite /var/cache/apt/archives/python3.7-distutils_3.7.9-1+focal1_all.deb
#RUN apt-get -f install 

RUN apt-get install -y libsm6 libxext6 libxrender-dev

# https://github.com/yaroslavvb/tensorflow-community-wheels/issues/206
COPY requirements.txt .
RUN python3.7 -m pip install -r requirements.txt

# COPY tensorflow-2.7.0-cp37-cp37m-linux_x86_64.whl .
# RUN python3.7 -m pip install --ignore-installed --upgrade tensorflow-2.7.0-cp37-cp37m-linux_x86_64.whl

# RUN apt-get install -y python3-protobuf

EXPOSE 9100
