# VERSION   0.1
FROM        paultag/uwsgi:latest
MAINTAINER  Paul R. Tagliamonte <paultag@debian.org>

RUN echo "deb-src http://http.debian.net/debian/ unstable main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    python3.4 python3-pip \
    git \
    uwsgi-plugin-python3 \
    libpq-dev libgeos-dev

RUN apt-get update && apt-get build-dep -y python3-psycopg2
RUN mkdir -p /opt/pault.ag/
ADD . /opt/pault.ag/api.pault.ag/
RUN python3.4 /usr/bin/pip3 install -r /opt/pault.ag/api.pault.ag/requirements.txt

WORKDIR /opt/pault.ag/api.pault.ag/
