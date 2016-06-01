#!/usr/bin/python

import os
import os.path
for root, dirs, files in os.walk("/home/nfs/xiaowei/docker/"):
    for name in files:
        print os.path.join(root, name)
