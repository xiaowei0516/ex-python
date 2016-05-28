'''

1£©һ¸ö_init__()£¬Õ¸����¨ÊÔÎÃ¸øº¯Êdecoratorʱ±»µ÷¬ËÒ£¬ÐҪÓһ¸öĲÎýÍǱ»decoratorµĺ¯Ê¡£
2£©һ¸ö_call__()£¬Õ¸����¨ÊÔÎÃµ÷»decoratorº¯Êʱ±»µ÷ġ£
'''


class myDecorator(object):
    def __init__(self, fn):
        print "enter __init"
        self.fn = fn

    def __call__(self):
        self.fn()
        print "enter call"

@myDecorator
def aFunc():
    print "enter afunc"


print "**************************"
aFunc()
