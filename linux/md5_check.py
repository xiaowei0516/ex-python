#!/usr/bin/python
import  hashlib
def get_file_md5(filename=''):
    with open(filename, 'r') as f:
        m = hashlib.md5()
        while True:
            data = f.read(10240)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def md5_check(md5file="all.md5"):
    with open(md5file,'r') as  fileHandle:
        fileList = fileHandle.readlines()
        for fileLine in fileList:
            if ".md5" not in fileLine:
                arr = fileLine.strip().split()
                if arr[0] !=  get_file_md5(arr[1]):
                    return  "False"
        return "Ok"
                         
                         

print md5_check()
