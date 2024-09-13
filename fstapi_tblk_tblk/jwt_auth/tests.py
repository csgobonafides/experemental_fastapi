import time
from datetime import timedelta, datetime

a = datetime.now() + timedelta(days=0, seconds=5)
b = datetime.now()

while a > b:
    b += timedelta(days=0, seconds=1)
    print('s')
    time.sleep(1)