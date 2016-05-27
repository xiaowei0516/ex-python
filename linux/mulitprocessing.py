#!/usr/bin/python
import os
'''
#os.fork  be used in linux kernel interrelate (eg:linux,Mac), not used in windows
#but multiprocessing library use cross-platform

print 'Process (%s) start'  % os.getpid()

pid = os.fork()

if pid == 0:
    print "child process (%s) and my parent is %s" %(os.getpid(), os.getppid())
else:
    print "parent (%s) created a child process (%s)" %(os.getpid(), pid)

'''
from multiprocessing import Process
import os

def run_proc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())

if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Process(target=run_proc, args=('test',))
    print 'Process will start.'
    p.start()
    p.join()
    print 'Process end.'
