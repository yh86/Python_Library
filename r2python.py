# 
# Test script for running Python script inside R console
#       system('python r2python.py')
#

import time, socket, datetime

print 'This is a test for calling Python script from within R console'
print socket.gethostname()
print time.strftime("%Y-%b-%d  %H:%M:%S")
print 'Test successful'