def func(name, *args, **kwds):
    print "name type:", type(name)
    print "args type:", type(args)
    print "kwds type:", type(kwds)
    print "name :", (name)
    print "args :", (args)
    print "kwds :", (kwds)
    call(name, *args, **kwds)

def call(name, age, address, no='aabb', num=99):
    print "name=",name
    print "age=",age
    print "no=",no
    print "num=",num

func("xiaowei",'12','wx', no='aa',num=88)
