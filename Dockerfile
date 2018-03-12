FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
    python3-pip

WORKDIR /vv
COPY . /vv

RUN pip3 install -r requirements.txt

RUN apt-get remove -y wget rpcbind busybox

RUN useradd -ms /usr/sbin/nologin appuser
USER appuser

CMD ["python3", "/vv/run.py"]