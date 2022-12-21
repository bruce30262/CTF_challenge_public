#!/usr/bin/env python3
import os
import subprocess as sp

to_kill = [b'setup.sh', b'node', b'socat']

"""
bruce30+   56901  0.0  0.0  10100  3988 pts/3    S    21:39   0:00 /bin/bash ./setup.sh
bruce30+   56939  0.0  0.0  10100  2288 pts/3    S    21:39   0:00 /bin/bash ./setup.sh
bruce30+   56944  0.0  0.2 614412 38012 pts/3    Sl   21:39   0:00 node /usr/bin/static -a 0.0.0.0 -p 8080
bruce30+   56945  0.0  0.0  10284  2980 pts/3    S    21:39   0:00 socat tcp-listen:30263,fork,reuseaddr,bind=0.0.0.0 exec:./run.sh
"""

PS = sp.check_output('ps -eax -o pid,comm', shell=True).strip().split(b"\n")
for l in PS:
    info = l.strip().split(b" ")
    pid, comm = info[0], info[1]
    if comm in to_kill:
        cmd = f"kill -9 {pid.decode()}"
        print(cmd, comm.decode())
        os.system(cmd)
print("Done")
