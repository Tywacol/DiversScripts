#!/usr/bin/env python
import os
import sys
b = 0
a = int(sys.argv[1])  
b = int(sys.argv[2])


for i in range(a) :
	os.system("amixer -D pulse sset Master 1%-;sleep 60")
print("Bonne nuit!")
os.system("shutdown now")
