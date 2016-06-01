#!/usr/bin/python
import hashlib

def get_file_md5(f):
    m = hashlib.md5()
    while True:
        data = f.read(10240)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

if __name__ == '__main__':
    YOUR_FILE = "/home/nfs/xiaowei/github/ex-python/linux/a.py"
    with open(YOUR_FILE, 'r') as f:
        file_md5 = get_file_md5(f)
        print file_md5
