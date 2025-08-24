#!/bin/sh
qemu-system-aarch64 \
  -M virt \
  -cpu max \
  -nographic \
  -m 1024M \
  -kernel Image \
  -initrd initramfs.cpio.gz \
  -append "console=ttyAMA0 rdinit=/linuxrc" \
  -net user,hostfwd=tcp:0.0.0.0:31337-:31337 \
  -net nic,model=e1000 \
  -monitor /dev/null

