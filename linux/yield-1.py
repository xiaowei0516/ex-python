#-*- coding:utf-8 -*-


def foo():
    yield 1
    print "hhhhhhhhhhhhhh--sep--"
    yield 2
p=foo()
print p
print p.next()
print p.next()






#函数没有用return 返回值，用yield 输出值，函数的调用返回值为生成器对象，
#生成器对象，用p.next()方法返回一个值，函数执行暂停，下次再调用next()方法时，从
#暂停处开始执行，print 输出值。再执行第二个yield 返回值。
#像上面函数的返回值为生成器对象的函数叫做生成器函数。

