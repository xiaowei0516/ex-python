#-*- coding:utf-8 -*-

def func_var_args(fargs, *args):
    print "fargs:",fargs
    for value in args:
        print "arg:",value

func_var_args(1,2,3,4,'abc',None)
func_var_args(233)
