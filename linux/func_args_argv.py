#-*- coding:utf-8 -*-
def func_args_argv(*args, **argv):
    print "args:", args
    print "argv:", argv

args=[1,2,3,4]
argv={"name":"hellokitty", "age":"25"}

func_args_argv(args, argv)

func_args_argv(1,2,3,a=100)


func_args_argv(*args, **argv)
