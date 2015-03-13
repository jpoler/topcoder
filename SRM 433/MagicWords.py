# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class KMP:
    def __init__(self, p):
        self.p = list(p)
        self.compute_prefix()
        
    def compute_prefix(self):
        self.shifts = [1] * (len(self.p) + 1)
        shift = 1
        for pos in range(len(self.p)):
            while shift <= pos and self.p[pos] != self.p[pos-shift]:
                shift += self.shifts[pos-shift]
            self.shifts[pos+1] = shift

    def match(self, text):
        matches = []
        start_pos = 0
        match_len = 0
        for c in text:
            while match_len == len(self.p) or \
                  match_len >= 0 and self.p[match_len] != c:
                start_pos += self.shifts[match_len]
                match_len -= self.shifts[match_len]
            match_len += 1
            if match_len == len(self.p):
                matches.append(start_pos)
        return matches
            
        
            


class MagicWords:

    def count(self, S, K):
        print()
        print("S", S)
        print("K", K)
        ans = 0
        orig = "".join(S)
        perm = itertools.permutations(S)

        kmp = KMP(orig)
        
        for p in perm:
            joined = "".join(p)
            double = joined + joined
            res = kmp.match(double)
            if res: ans += 1

        return ans

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

def do_test(S, K, __expected):
    startTime = time.time()
    instance = MagicWords()
    exception = None
    try:
        __result = instance.count(S, K);
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
    sys.stdout.write("MagicWords (250 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("MagicWords.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            S = []
            for i in range(0, int(f.readline())):
                S.append(f.readline().rstrip())
            S = tuple(S)
            K = int(f.readline().rstrip())
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(S, K, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1425956012
    PT, TT = (T / 60.0, 75.0)
    points = 250 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
