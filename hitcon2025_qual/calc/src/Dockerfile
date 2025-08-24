FROM debian:12
MAINTAINER bruce30262
RUN apt update
RUN apt upgrade -y
RUN apt install -y qemu-system-aarch64
RUN useradd -m user
COPY ./chal /home/user
WORKDIR /home/user
CMD ["/home/user/run.sh"]
