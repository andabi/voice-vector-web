FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
    python-pip python3-pip

RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:mc3man/trusty-media

RUN apt-get update && \
    apt-get install -y \
    ffmpeg

WORKDIR /vv
COPY . /vv

RUN pip3 install -r requirements.txt
RUN pip3 install grpcio
RUN pip2 install tensorflow-serving-api

RUN cp -r /usr/local/lib/python2.7/dist-packages/tensorflow_serving /usr/local/lib/python3.5/dist-packages/tensorflow_serving
RUN cp -r /usr/local/lib/python2.7/dist-packages/tensorflow_serving_api-1.5.0.dist-info/ /usr/local/lib/python3.5/dist-packages/tensorflow_serving_api-1.5.0.dist-info

RUN apt-get remove -y wget rpcbind busybox

RUN useradd -ms /usr/sbin/nologin appuser
USER appuser

CMD ["python3", "/vv/run.py"]