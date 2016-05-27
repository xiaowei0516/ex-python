#!/usr/bin/python

import subprocess
proc = subprocess.call(['ls', '-l'])
print type(proc)
print proc
