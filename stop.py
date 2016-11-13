from subprocess import Popen, PIPE
import os

"""
This script if for stoping processes within this project
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

if len(sys.argv) < 2:
    print "usage: python stop.py [environment]"
    print "environment:\t production|testing|development"
    sys.exit(os.EX_USAGE)

ENVIRONMENT = sys.argv[1]

if ENVIRONMENT == 'production':
    port = 8096
else:
    port = 8095

p = Popen(['lsof', '-i:{0}'.format(port)], stdout=PIPE)
output = p.communicate()[0].split("\n")

process = []

titles = ' '.join(output[0].split()).split()

for i in xrange(1, len(output) - 1):
    data = ' '.join(output[i].split()).split()
    item = {}
    for j in xrange(len(titles)):
        item[titles[j]] = data[j]
    process.append(item)

# kill all process
for each in process:
    print "stoping tornado process " + each["PID"]
    os.system("kill " + each["PID"])
