#!/usr/bin/python
# encoding: utf-8  

import tarfile  
import os  
import time  
  
start = time.time()  
tar=tarfile.open('/home/nfs/xiaowei/aa.tar.gz','w')  
for root,dir,files in os.walk('/home/nfs/xiaowei/iprobe-3.x'):  
         for file in files:  
                 fullpath=os.path.join(root,file)  
                 tar.add(fullpath,arcname=file)  
tar.close()  

print time.time()-start 




 
