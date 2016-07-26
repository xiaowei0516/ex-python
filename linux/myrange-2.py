#-*- coding:utf-8 -*-
class Zrange:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return ZrangeIterator(self.n)

#iterator class
class ZrangeIterator:
    def __init__(self, n):
        self.i = 0
        self.n = n
    def __iter__(self):
        return self
    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration() 

zrange = Zrange(3)
print zrange is iter(zrange)   

print [i for i in zrange]
print [i for i in zrange]




#list类型也是按照上面的方式，list本身是一个可迭代对象，通过iter()方法可以获得list的迭代器对象

li=[1,2,3]
print li is iter(li)

print "__iter__" in dir(li)
print "__iter__" in dir(iter(li))
print "next" in dir(iter(li))
