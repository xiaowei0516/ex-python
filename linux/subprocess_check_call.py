#!/usr/bin/python

import subprocess
proc = subprocess.check_call(['ls', '-l'])
print type(proc)
print proc
