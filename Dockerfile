FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
    python3-pip

RUN pip3 install flask flask-compress requests

WORKDIR /vv
COPY . /vv

RUN apt-get remove -y wget rpcbind busybox

RUN useradd -ms /usr/sbin/nologin appuser
USER appuser

CMD ["python3", "/vv/run.py"]