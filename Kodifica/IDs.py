# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

F = fractions.Fraction

class IDs:
    def prob_collision(self, n, k, collisions):
        return (n-F(collisions))/F(math.pow(n, collisions))

    def collisionProbability(self, num, counts):
        n = F(num)
        k = F(sum(counts))
        print()
        print(repr(n), repr(k))
        ans = F(0.0)
        if n < k:
            return 1.0
        for i in range(2, int(min(k, 5))):
            p = self.prob_collision(n, k, F(i))
            print("prob", p)
            c = self.choose(k, F(i))
            print("combinations", c)
            print(type(p), type(c))
            print("p*c", repr(p*c))
            ans += p*c
        print("ans", repr(ans))
        print("float ans", float(ans))
        return float(ans)
            

    def choose(self, n, k):
        result = F(1.0)
        for i in range(1, int(k+1)):
            result *= F(n - (k - i))/F.from_float(float(i))
        return result

        


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

def do_test(num, counts, __expected):
    startTime = time.time()
    instance = IDs()
    exception = None
    try:
        __result = instance.collisionProbability(num, counts);
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
    sys.stdout.write("IDs (500 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("IDs.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            num = int(f.readline().rstrip())
            counts = []
            for i in range(0, int(f.readline())):
                counts.append(int(f.readline().rstrip()))
            counts = tuple(counts)
            f.readline()
            __answer = float(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(num, counts, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1426178446
    PT, TT = (T / 60.0, 75.0)
    points = 500 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
