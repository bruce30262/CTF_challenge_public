* This isn't a kernel challenge. Try get shell.
* Challenge binary is at /home/user/calc after decompressing initramfs.cpio.gz. Flag is under /home/user/ .
* To launch the service, cd into this directory and `docker compose up -d`. After that you should be able to connect to service with localhost:31337.
* It is highly recommended to use the provided docker environment to solve the challenge. 
  - If you want to run the `qemu-system-aarch64` command directly, make sure you're using the same version in docker container ( version 7.2.17 ). Newer version ( e.g. version 8.2.2 in Ubuntu 24.04 ) might crash if you run `run.sh` directly.