FROM ubuntu:18.04
MAINTAINER bruce30262
# install dependencies
RUN apt-get update
RUN apt-get install -y git vim wget locales

# For running challenge
RUN apt-get install -y xinetd binutils libstdc++6 libc6 python-pip python2.7

# misc tools
RUN apt-get update && apt-get install -y \ 
    iptables \
    iputils-ping \
    net-tools \
    netcat

# Set the locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# Set privilege for some dir
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN useradd -m emojivm -d /home/emojivm/

# COPY challenge source, set permission
COPY ./opt/ /opt/
RUN chmod -R 700 /opt/service/
RUN chmod -R 700 /opt/log/
RUN chmod -R 711 /opt/files/
RUN chown -R root:root /home/emojivm

# Restrict emojivm's permission
RUN chmod 700 /bin/*
RUN chmod 711 /bin/
RUN chmod +x /bin/ls
RUN chmod +x /bin/pwd
RUN chmod +x /bin/cat
RUN chmod +x /bin/sh
RUN chmod +x /bin/bash

CMD ["/usr/sbin/xinetd","-dontfork"]

