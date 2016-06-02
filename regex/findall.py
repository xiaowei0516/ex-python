#!/usr/bin/python
import re

#regular expression is compiled into an Pattern object

pattern = re.compile(r'\d+')
#Pattern matching using text, obtained matching result, if not match return None

match_list = pattern.findall('www1ttt2dd5')

print match_list
