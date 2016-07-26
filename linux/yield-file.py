#-*- coding:utf-8 -*-

import time
start_time = time.time()


def find_ip(path):
    for line in open(path):
        s = line.find('yield')
        print s
        if s >= 0:
            yield line[:s].strip()

p = find_ip("yield-2.py")

print "--------------------------"
print list(p)  # p 

#set is  not-repeat operation

p = list(set(list(p)))
for item in p:
    print item

