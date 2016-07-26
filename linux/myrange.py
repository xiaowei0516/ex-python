#!/usr/bin/env Python
# coding=utf-8

"""
the interator as range()
"""
class MyRange(object):
    def __init__(self, n):
        self.i = 0
        self.n = n
        print "aa"

    def __iter__(self):
        print "bbbb"
        return self

    def next(self):
        if self.i < self.n:
            print "cccc"
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()

if __name__ == "__main__":
    x = MyRange(7)
    print "x.next()==>", x.next()
    print "x.next()==>", x.next()
    print "------for loop--------"
    for i in x:
       print i
