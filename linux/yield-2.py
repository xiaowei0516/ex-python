#-*- coding:utf-8 -*-

#enhance generators
#use send transmit parameter to yield

def foo():
    number = 0
    while True:
        val = yield number
        print "gggggg-sep----"
        if  val:
            number = val
        else:
            number += 1
        print val
p = foo()
print p.next()
print p.send(2)
#print p.next()
