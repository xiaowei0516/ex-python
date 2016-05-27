#!/usr/bin/python

#this process, cpu usage  not  eq  (100% * cpu_count) ,because python Interpreter realize GIL lock, not use all core

import threading, multiprocessing

def loop():
    x = 0
    while True:
        x = x ^ 1


print multiprocessing.cpu_count()
for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()
