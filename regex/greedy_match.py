#!/usr/bin/python
import re

#regular expression is compiled into an Pattern object

pattern = re.compile(r'(\d+)(0*)$')
#Pattern matching using text, obtained matching result, if not match return None

match = pattern.match('10234500')
print match

print match.groups()
