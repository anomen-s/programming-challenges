import signal
import time

# disable QUIT ctrl+\
signal.signal(signal.SIGQUIT, lambda a, b: None)


time.sleep(1000)
