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

# Add user
RUN useradd -m ctf -d /home/ctf/
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

# COPY challenge source, set permission
COPY ./opt/ /opt/
RUN mkdir -p /opt/log/
RUN chown -R ctf:ctf /opt/log/
RUN chown ctf:ctf /opt/run.sh

CMD ["/usr/sbin/xinetd","-dontfork"]

