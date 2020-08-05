import sys

vystup = open("/tmp/python-out.txt", "wt")
print("x 1")
print("x 2", file=vystup)


oldout = sys.stdout
sys.stdout = vystup
print("x 3")
sys.stdout = oldout

vystup.close()
