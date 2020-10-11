import time
import os
from pathlib import Path

home_path: str = str(Path.home())
home_path = f"{home_path}/cron"

if not os.path.exists(home_path):
    os.makedirs(home_path)

os.chdir(home_path)
beats = "beats.txt"
t = time.time()
log = open(beats, "a")
log.write(str(t) + "\n")
log.close()