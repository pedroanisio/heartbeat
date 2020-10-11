import time
import os

# os.chdir("/home/udi/foo")

beats = "beats.txt"
t = time.time()
log = open(beats, "a")
log.write(str(t)+"\n")
log.close()