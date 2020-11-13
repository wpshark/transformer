FROM python:2.7.17

ENV DEBIAN_FRONTEND noninteractive
RUN export DEBIAN_FRONTEND=noninteractive

ADD requirements.txt /tmp/requirements.txt
RUN pip install pip -U && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

VOLUME /usr/src/app
WORKDIR /usr/src/app

CMD /usr/src/app/docker/bootstrap.sh
