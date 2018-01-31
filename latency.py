import re
import os
import shlex
from subprocess import Popen, PIPE, STDOUT

def cmd_output(cmd, stderr=STDOUT):
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]

def ping_time(host):
    try:
        cmd = "fping {host} -C 3 -q".format(host=host)
        res = cmd_output(cmd)
        ints = re.search(r"(\d+\.\d+)\s(\d+\.\d+)\s(\d+\.\d+)", str(res))
        intssum = float(ints[1]) + float(ints[2]) + float(ints[3])
        avg = ("%.4f" % (intssum / 3 / 1000))
        adjlatency=(float(4)*float(avg))
        return adjlatency
    except:
        return "latency test failed"
