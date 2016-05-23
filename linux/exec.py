#!/usr/bin/python
import subprocess
def Exec(cmd, close_fds=True):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return p.communicate()[0]
    except Exception,e:
        print "Exec failed,command:%s, error %s" %(cmd, str(e))
        return None


if __name__ == '__main__':
    ret = Exec("time")
    print ret
