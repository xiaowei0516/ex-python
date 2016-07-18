#!/usr/bin/env python
import os,sys
r,w = os.pipe()
pid = os.fork()

if pid:  #father
    os.close(w)
    r = os.fdopen(r)
    print "parent:reading"
    txt = r.read()
    os.waitpid(pid,0) # child process exit
else:
    os.close(r)
    w=os.fdopen(w,'w')
    print "child:writing"
    w.write("hello china")
    w.close()
    sys.exit(0)
print "parent: texe=",txt
