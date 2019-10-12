def long_function_call():
	s=0
	for i in range(100000000):
		s+=i
	print(i)

import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")

signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(2)   # timeout seconds
try:
    long_function_call()
except Exception as i:
    print(i.args[0])
    

