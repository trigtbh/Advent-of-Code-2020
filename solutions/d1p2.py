import os
base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
def read(i):
    with open(os.path.join(base, "inputs", "d" + str(i) + ".txt")) as f:
        return f.read()

text = read(1)
nums = [int(x) for x in text.split('\n')]

for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        for k in range(j + 1, len(nums)):
            if nums[i] + nums[j] + nums[k] == 2020:
                print(nums[i] * nums[j] * nums[k])
                break
        else:
            continue
        break
    else:
        continue
    break
