#! /usr/bin/python
print "Content-Type: text/html\n"

import os

info = os.environ
for x in info.keys():
    print x + ": " + info[x] + "<br>"
