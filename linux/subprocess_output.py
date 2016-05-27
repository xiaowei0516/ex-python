#!/usr/bin/python

import subprocess
proc = subprocess.check_output(['ls', '-l'])
print type(proc)
