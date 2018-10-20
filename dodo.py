#!/usr/bin/env python3
import os
import sys
import time

duration = 60
if len(sys.argv) > 1 :
	time = sys.argv[1]
for i in range(duration) :
	time.sleep(60)
	os.system("amixer set 'Master' 1%-")

os.system("shutdown now")
