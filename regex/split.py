#!/usr/bin/python
import re

#regular expression is compiled into an Pattern object

pattern = re.compile(r'\s+')
#Pattern matching using text, obtained matching result, if not match return None

match = pattern.split('hello world')
print match
