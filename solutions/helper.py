import os
base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
def read(i):
    with open(os.path.join(base, "inputs", "d" + str(i) + ".txt")) as f:
        return f.read()