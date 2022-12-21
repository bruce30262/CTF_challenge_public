# Before you start

In order to solve this challenge, you'll need the flags from the other Fourchain challenges ( Hole, Sandbox, Kernel & Hypervisor ), so make sure you complete them first before starting on this one.

# Goal

The goal is to combine the exploits you've created for the previous Fourchain challenges into a fullchain exploit and pwn a remote VM.

If you successfully escape VirtualBox in the end, the flag will be at host's `/flag`.

# Environment

We've prepared a Vagrant VM for this challenge. It is recommended that you run this VM on Debian Linux 11.5.0 .  

There are three folders in this attachment : Browser, VirtualBox and Vagrant. Each folder includes a README.txt, make sure you read them all before setting up the environment.

# About remote service

To prove that you're qualified for solving this challenge, the remote service will ask you to input the flags information of the previous Fourchain challenges after you pass the hashcash POW.  

For example:

* Hole's flag: hitcon{111}
* Sandbox's flag: hitcon{222}
* Kernel's flag: hitcon{333}
* Hypervisor's flag: hitcon{444}

You will need to input a single line of sha256 hash value in order to prove that you have these four flags:

sha256sum("hitcon{111}hitcon{222}hitcon{333}hitcon{444}")

After you pass the hashcash POW & the flag checking, the service will try to create a remote VM for you. It'll take about 3 minutes to boot up the VM and launch the service. 

If everything goes well, the service will give you the IP & port of the remote VM, then you can start the exploitation.

# About remote VM  

The remote VM will only last for about 10 minutes, after that we'll delete the remote VM, and you'll have to use the remote service to request another VM.  

Notice that we'll only:

* Create the remote VM for you.
* Delete the remote VM after 10 minutes.

Other than that, you're on your own. 

If you screwed up the VM during exploitation and couldn't connect to the service anymore, there's nothing we can do about it, so make sure you test your exploits at local side before attacking the remote VM.


Finally, we've spent lots of time and resources to create this challenge, so please, be nice and DO NOT attack our infrastructure.


Enjoy, and good luck :)
