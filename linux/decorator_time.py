#-*- coding-utf8 -*-

import datetime
def GetRunTime(func):
    def check(*args, **argv):
        startTime = datetime.datetime.now()
        f = func(*args, **argv)
        endTime = datetime.datetime.now()
        print(endTime - startTime)
        return f
    return check
@GetRunTime
def test():
    print "HELLO KITTY"

test()
