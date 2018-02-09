#!/usr/bin/python

import sys

if len(sys.argv)==2:
    print("Knock, Knock, {0}".format(sys.argv[1]))
else:
    sys.stderr.write("Usage : {0} <name>\n".format(sys.arv[0]))
