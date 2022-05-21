import sys
from colorama import Fore, Back, Style
import contextlib, io
import traceback
import difflib
import inspect
import time

from functools import wraps

renderall = []
canon = []

global toggle_off
toggle_off = False

global success
global failure
global total
success = 0
failure = 0
total = 0

def toggle():
    global toggle_off
    toggle_off = not(toggle_off)

def linebreak():
    def blank():
        print("")
    renderall.append(blank)

times = []

def test(params=None, stdin=None, stdout=None, return_val=None):
    
    if stdin is None:
        stdin = ""
    if stdout is None and return_val is None:
        raise TypeError("function test missing output data to compare to")
        return
    def decorate(function):
        @wraps(function)
        def inner(*args, **kwargs):
            global success, failure, total
            f = io.StringIO()

            temp = Style.BRIGHT + "  -->" + Style.RESET_ALL + " Running test " + str(len(times) + 1) + "/" + str(len(canon)) + " (" + function.__name__ + ")..."
            print(temp, end="\r")
            #err = io.StringIO()
            raised = False
            error = ""
            failed_value = False
            delta = 0
            with contextlib.redirect_stdout(f):
                
                try:
                    if len(inspect.getargspec(function)[0]) > 0:
                        start = time.time()
                        v = function(*params)
                    else:
                        oldstdin = sys.stdin
                        sys.stdin = io.StringIO(stdin)
                        start = time.time()
                        v = function()
                    if return_val and v != return_val:
                        failed_value = True
                except Exception as e:    
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                    error = (''.join(tb.format_exception_only()))
                    raised = True
                delta = round(time.time() - start, 7)
                times.append(delta)
            output = f.getvalue()

            if output.endswith("\n"):
                output = "\n".join(output.split("\n")[:-1])
            print("\r" + (" " * (len(temp) + 1)) + "\r", end="")
            if raised:
                
                print("[ " + Fore.RED + Style.BRIGHT + "X" + Style.RESET_ALL + " ] Test failed: " + Fore.RED + Style.BRIGHT + function.__name__ + " (" + str(delta) + "s)" + Style.RESET_ALL)
                print("\t" + Fore.RED + Style.BRIGHT + "Exception raised\n\t" + Style.RESET_ALL + str(error).strip())
                
                failure += 1
            elif failed_value:
                print("[ " + Fore.RED + Style.BRIGHT + "X" + Style.RESET_ALL + " ] Test failed: " + Fore.RED + Style.BRIGHT + function.__name__ + " (" + str(delta) + "s)" + Style.RESET_ALL)
                expectedlines = str(return_val).split("\n")
                print("\tExpected: ", end="")
                print(expectedlines[0])
                for line in expectedlines[1:]:
                    print("\t          " + line)

                chars = []
                
                difference = [c for c in difflib.ndiff(str(return_val), str(v))]
                out = False
                for c in difference:
                    mod = c[0]
                    char = c[-1]
                    if mod == "+" and not out:
                        chars.append(Back.RED)
                        chars.append(Style.BRIGHT)
                        out = True
                    if mod == " " and out:
                        chars.append(Style.RESET_ALL)
                        out = False
                    if mod != "-":
                        chars.append(char)
                chars.append(Style.RESET_ALL)

                returned = "".join(chars)
                rlines = returned.split("\n")
                print("\tReturned: ", end="")
                print(rlines[0])
                for line in rlines[1:]:
                    print("\t          " + line)
                failure += 1
            elif stdout != output and return_val is None:
                print("[ " + Fore.RED + Style.BRIGHT + "X" + Style.RESET_ALL + " ] Test failed: " + Fore.RED + Style.BRIGHT + function.__name__ + " (" + str(delta) + "s)" + Style.RESET_ALL)
                expectedlines = stdout.split("\n")
                print("\tExpected: ", end="")
                print(expectedlines[0])
                for line in expectedlines[1:]:
                    print("\t          " + line)

                chars = []
                
                difference = [c for c in difflib.ndiff(stdout, output)]
                out = False
                for c in difference:
                    mod = c[0]
                    char = c[-1]
                    if mod == "+" and not out:
                        chars.append(Back.RED)
                        chars.append(Style.BRIGHT)
                        out = True
                    if mod == " " and out:
                        chars.append(Style.RESET_ALL)
                        out = False
                    if mod != "-":
                        chars.append(char)
                chars.append(Style.RESET_ALL)

                returned = "".join(chars)
                rlines = returned.split("\n")
                print("\tReturned: ", end="")
                print(rlines[0])
                for line in rlines[1:]:
                    print("\t          " + line)
                failure += 1
            else:
                print("[ " + Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL + " ] Test passed: " + Fore.GREEN + Style.BRIGHT + function.__name__ + " (" + str(delta) + "s)" + Style.RESET_ALL)
                success += 1
            total += 1
        renderall.append(inner)
        canon.append(inner)
        return inner
    return decorate

def render(time_limit=None):
    global success, failure, total, toggle_off
    if not toggle_off:
        print("[ " + Style.BRIGHT + "*" + Style.RESET_ALL + " ] Beginning tests\n---")
        for config in renderall:
            config()
        total_time = round(sum(times), 7)
        timestr = str(total_time) + "s"
        timego = True

        if time_limit:
            if total_time > time_limit:
                timego = False
                timestr = Back.RED + Style.BRIGHT + timestr + Style.RESET_ALL
            else:
                timestr = Fore.GREEN + Style.BRIGHT + timestr + Style.RESET_ALL
        print("---\n[ " + Style.BRIGHT + "*" + Style.RESET_ALL + " ] " + "All tests complete (" + timestr + ").")
        color = ""
        if total == 0:
            color = Fore.GREEN
        elif int(success / total) == 1 and timego:
            color = Fore.GREEN
        elif success == 0 or not timego:
            color = Fore.RED
        
        print(color + Style.BRIGHT + "[ * ] " + str(success) + "/" + str(total) + " tests passed." + Style.RESET_ALL)