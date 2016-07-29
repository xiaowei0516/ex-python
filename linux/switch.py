#-*- coding : utf-8 -*-

def start():
    print "start"
    pass
def stop():
    print "stop"
    pass
def restart():
    print "restart"
    pass

switch={
"start": start,
"stop": stop,
"restart": restart
}

print type(switch["start"])
print type(start)

switch["start"]()


