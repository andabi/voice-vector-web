FROM idock.daumkakao.io/kakaobrain/zeze_base:v1

RUN apt-get install -y python-pip
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:mc3man/xerus-media

RUN apt-get update -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y \
    ffmpeg

RUN pip3 install grpcio
RUN pip2 install tensorflow-serving-api==1.5.0

COPY ./requirements.txt  /requirements.txt
RUN pip3 install -r /requirements.txt

RUN cp -r /usr/local/lib/python2.7/dist-packages/tensorflow_serving /usr/local/lib/python3.5/dist-packages/tensorflow_serving
RUN cp -r /usr/local/lib/python2.7/dist-packages/tensorflow_serving_api-1.5.0.dist-info/ /usr/local/lib/python3.5/dist-packages/tensorflow_serving_api-1.5.0.dist-info

RUN apt-get remove -y wget rpcbind busybox

WORKDIR /vv
COPY . /vv

RUN useradd -ms /usr/sbin/nologin appuser
RUN chown -hR appuser /vv/voice_file
USER appuser

CMD ["python3", "/vv/run.py"]