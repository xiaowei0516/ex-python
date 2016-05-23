#!/usr/bin/env python  
  
import os,sys,subprocess  
  
def update(path):  
    f = open(file,'w')  
    for root,dirs,files in os.walk(path):  
        for name in files:  
            line = os.path.join(root, name)  
            (stdin,stderr) = subprocess.Popen(['md5sum',line],stdout=subprocess.PIPE).communicate()  
            f.write(stdin)  
    f.close()  
  
def check(path):  
    f = open(file,'r')  
    for line in f:  
        line = line.strip()
        check_ok = """echo '%s' | md5sum -c > /dev/null 2>&1""" % line  
        print check_ok  
        if not subprocess.call(check_ok, shell = True) == 0:  
            abnormal = line.split()  
            print abnormal[1]  
    f.close()  
  
def Usage():  
    print ''' 
    Usage: python %s update /home/wwwroot 
           python %s check /home/wwwroot 
    ''' % (sys.argv[0],sys.argv[0])  
    sys.exit() 

if __name__ == '__main__': 
    if len(sys.argv) != 3:  
        Usage()  
  
    file = 'all.md5'  
    model = sys.argv[1]  
    path = sys.argv[2]  
  
    if os.path.exists(path) == False:  
        print "\033[;31mThe directory or file does not exist\033[0m"  
        sys.exit()  
    elif model == 'update':  
        update(path)  
    elif model == 'check':  
        check(path)  
    else:  
        Usage()  
