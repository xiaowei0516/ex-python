#-*- coding:utf-8 -*-

def func_var_args(fargs, **argv):
    print "fargs:",fargs
    for key in argv:
        print "key:%s, value:%s" %(key,argv[key])

func_var_args(1,ma="aa",mb="bb",mc="cc")
func_var_args(233)
