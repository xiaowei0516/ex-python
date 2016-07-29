from functools import wraps
def logged(func):
    print "11111111111111111"
    @wraps(func)
    def with_logging(*args, **kwargs):
        print "333333333333333"
        print func.__name__
        print "22222222222222222"
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   """does some math"""
   return x + x * x

print (f.__name__)  # prints 'f'
print (f.__doc__)   # prints 'does some math'
x=5
f(x)
