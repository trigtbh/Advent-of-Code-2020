import easytest as et
from colorama import Fore, Style
from io import StringIO
import contextlib

import os
os.system("clear")

import time

print(f"[ {Style.BRIGHT}*{Style.RESET_ALL} ] Beginning tests")
print("---")

passed = 0
failed = 0
rtime = 0.0

from solutions import helper

for i in range(25):
    start = time.time()
    f = StringIO()
    try:
        with contextlib.redirect_stdout(f):
            __import__(f"solutions.d{i+1}p1")
    except Exception as e:
        failed += 1
        delta = time.time() - start
        rtime += delta
        print(f"[ {Fore.RED + Style.BRIGHT}X{Style.RESET_ALL} ] Day {i+1} test failed: {Style.BRIGHT + Fore.RED}day {i + 1} part 1 ({str(e)}){Style.RESET_ALL}")
        continue
    if i + 1 != 25:
        try:
            with contextlib.redirect_stdout(f):
                __import__(f"solutions.d{i+1}p2")
        except Exception as e:
            failed += 1
            delta = time.time() - start
            rtime += delta
            print(f"[ {Fore.RED + Style.BRIGHT}X{Style.RESET_ALL} ] Day {i+1} test failed: {Style.BRIGHT + Fore.RED}day {i + 1} part 2 ({str(e)}){Style.RESET_ALL}")
            continue
    delta = time.time() - start
    if delta > 15.0:
        failed += 1
        delta = time.time() - start
        rtime += delta
        print(f"[ {Fore.RED + Style.BRIGHT}X{Style.RESET_ALL} ] Day {i+1} test failed: {Style.BRIGHT + Fore.RED}day {i + 1} (total runtime: {round(delta, 3)}s){Style.RESET_ALL}")
    else:
        passed += 1
        print(f"[ {Fore.GREEN + Style.BRIGHT}✓{Style.RESET_ALL} ] Day {i+1} test passed: {Style.BRIGHT + Fore.GREEN}day {i + 1} (total runtime: {round(delta, 3)}s){Style.RESET_ALL}")
        rtime += delta

print("---")
print(f"[ {Style.BRIGHT}*{Style.RESET_ALL} ] All tests complete.")
color = ""
total = passed + failed
if total == 0:
    color = Fore.GREEN
elif int(passed / total) == 1:
    color = Fore.GREEN
elif passed == 0:
    color = Fore.RED

print(color + Style.BRIGHT + "[ * ] " + str(passed) + "/" + str(total) + " tests passed." + Style.RESET_ALL)