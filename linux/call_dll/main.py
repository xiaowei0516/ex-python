from  ctypes import *

#lib = ctypes.CDLL("libloop.so")
#lib.myprint()


lib = cdll.LoadLibrary("libloop.so")
lib.myprint()
