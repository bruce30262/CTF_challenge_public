FROM ubuntu:22.04
MAINTAINER bruce30262
# install dependencies
RUN apt-get update
RUN apt-get install -y locales

# For running challenge
RUN apt-get install -y xinetd python3

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
RUN useradd -m ctf -d /home/ctf/

# COPY challenge source, set permission
COPY ./opt/ /opt/
RUN chmod -R 700 /opt/service/
RUN chmod -R 711 /opt/files/
RUN chown -R root:root /home/ctf

CMD ["/usr/sbin/xinetd","-dontfork"]

