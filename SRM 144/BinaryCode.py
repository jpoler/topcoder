# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class BinaryCode:
    def decode(self, message):
        res = []
        res.append(self.decode_generic(message, 0))
        res.append(self.decode_generic(message, 1))
        return res

    def decode_generic(self, message, init):
        new_message = str(init)
        for i in range(1, len(message)):
            new_char = int(message[i-1]) - \
                       int(new_message[i-1]) - \
                       (int(new_message[i-2]) if i-2 >= 0 else 0)
            if new_char not in [0, 1]: return "NONE"
            new_message += str(new_char)

            if not self.check(new_message[i-1], i-1, message, new_message):
                return "NONE"
        if not self.check(new_message[len(message)-1], len(message)-1, message, new_message):
            return "NONE"
        return new_message

    def check(self, val, i, message, new_message):
        if i - 1 >= 0:
            l = int(new_message[i - 1])
        else:
            l = 0
        if i + 1 < len(message):
            r = int(new_message[i+1])
        else:
            r = 0
        res = int(message[i]) - l - r
        if str(res) == new_message[i]:
            return True
        return False
                

# CUT begin
# TEST CODE FOR PYTHON {{{
import sys, time, math

def tc_equal(expected, received):
    try:
        _t = type(expected)
        received = _t(received)
        if _t == list or _t == tuple:
            if len(expected) != len(received): return False
            return all(tc_equal(e, r) for (e, r) in zip(expected, received))
        elif _t == float:
            eps = 1e-9
            d = abs(received - expected)
            return not math.isnan(received) and not math.isnan(expected) and d <= eps * max(1.0, abs(expected))
        else:
            return expected == received
    except:
        return False

def pretty_str(x):
    if type(x) == str:
        return '"%s"' % x
    elif type(x) == tuple:
        return '(%s)' % (','.join( (pretty_str(y) for y in x) ) )
    else:
        return str(x)

def do_test(message, __expected):
    startTime = time.time()
    instance = BinaryCode()
    exception = None
    try:
        __result = instance.decode(message);
    except:
        import traceback
        exception = traceback.format_exc()
    elapsed = time.time() - startTime   # in sec

    if exception is not None:
        sys.stdout.write("RUNTIME ERROR: \n")
        sys.stdout.write(exception + "\n")
        return 0

    if tc_equal(__expected, __result):
        sys.stdout.write("PASSED! " + ("(%.3f seconds)" % elapsed) + "\n")
        return 1
    else:
        sys.stdout.write("FAILED! " + ("(%.3f seconds)" % elapsed) + "\n")
        sys.stdout.write("           Expected: " + pretty_str(__expected) + "\n")
        sys.stdout.write("           Received: " + pretty_str(__result) + "\n")
        return 0

def run_tests():
    sys.stdout.write("BinaryCode (550 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("BinaryCode.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            message = f.readline().rstrip()
            f.readline()
            __answer = []
            for i in range(0, int(f.readline())):
                __answer.append(f.readline().rstrip())
            __answer = tuple(__answer)

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(message, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1425784274
    PT, TT = (T / 60.0, 75.0)
    points = 550 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
