import os
base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
def read(i):
    with open(os.path.join(base, "inputs", "d" + str(i) + ".txt")) as f:
        return f.read()

text = read(1)
nums = [int(x) for x in text.split('\n')]

for n in nums:
    if (2020 - n) in nums:
        print(n * (2020 - n))
        break