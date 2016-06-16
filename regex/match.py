#!/usr/bin/python
import re

#regular expression is compiled into an Pattern object

pattern = re.compile(r'hello')
#Pattern matching using text, obtained matching result, if not match return None

match = pattern.match('hello world')

print type(match)

if match:
    print match.group()
