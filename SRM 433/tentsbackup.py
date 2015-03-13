# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

EVEN = False
ODD = True

class SettingTents:
    def __init__(self):
        self.memo = {}
        
    def rec(self, n, m):
        print("n:", n, "m:", m)
        if n <= 1 and m <= 1:
            print("returning 1")
            return 1

        total = 0
        if n <= 1:
            n_calls = [1]
            n_parity = ODD
        else:
            n_parity = n % 2
            half_n = n // 2
            if n_parity == EVEN:
                n_calls = [half_n]*2
            else:
                n_calls = [half_n, max(half_n - 1, 1)]
        if m <= 1:
            m_calls = [1]
            m_parity == ODD
        else:
            m_parity = n % 2
            half_m = m // 2
            if m_parity == EVEN:
                m_calls = [half_m]*2
            else:
                m_calls = [half_m, max(half_m -1, 1)]
        
        print(n_calls)
        print(m_calls)
        for i in n_calls:
            for j in m_calls:
                print("calculating:", i, j)
                try:
                    res = self.memo[(i, j)]
                except KeyError:
                    res = self.rec(i, j)
                    self.memo[(i, j)] = res
                    self.memo[(j, i)] = res
                total += res
        
        if n_parity == EVEN and m_parity == EVEN:
            total += 1
        if n_parity > 1 and m_parity > 1 and (n_parity == EVEN or m_parity == EVEN):
            total += 1
        print(self.memo)
        return total
        

    def countSites(self, N, M):
        print()
        print(N, M)
        locations = self.rec(N, M)
        print(locations)
        return locations

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

def do_test(N, M, __expected):
    startTime = time.time()
    instance = SettingTents()
    exception = None
    try:
        __result = instance.countSites(N, M);
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
    sys.stdout.write("SettingTents (500 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("SettingTents.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            N = int(f.readline().rstrip())
            M = int(f.readline().rstrip())
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(N, M, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1426110872
    PT, TT = (T / 60.0, 75.0)
    points = 500 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
