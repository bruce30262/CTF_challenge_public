It is recommended that you run this Vagrant VM on Debian Linux 11.5.0: https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-11.5.0-amd64-netinst.iso

If you really want to have the same kernel as our remote host, you can installed it from : http://ftp.debian.org/debian/pool/main/l/linux-signed-amd64/linux-image-5.10.0-19-cloud-amd64_5.10.149-2_amd64.deb

sha256sum of vmlinuz-5.10.0-19-cloud-amd64 : 668aacd08d7d0dba010b122a89fa8ad632a87d0958590b84b505fad93f25a002


Steps to build and run the VM:

* Install Vagrant and the vulnerable VirtualBox first ( check the VirtualBox directory ).  
* Copy the "chromium.tar.xz" from Browser/ into this directory.  
* Modify Vagrantfile for your own testing purpose.
* `vagrant up` to boot up the VM.
    - `nc localhost 31337` to check if the service is up.   
* `vagrant ssh` to login into the VM.  
* `vagrant destroy` to destroy the VM.