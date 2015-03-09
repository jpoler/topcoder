# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect, operator

CHOICES = 0
BLANKS = 1
SORTED = 2
UNIQUE = 3

class Lottery:
    def sortByOdds(self, rules):
        print()
        print(rules)
        res = []
        for rule in rules:
            print(rule)
            print(self.parse_rule(rule))
            name, [choices, blanks, sort, unique] = self.parse_rule(rule)

            if unique and sort:
                calc = self.binomial_coeff(choices, blanks)
            elif sort:
                calc = self.binomial_coeff(choices+blanks-1, blanks)
            elif unique:
                calc = self.binomial_coeff(choices, blanks)*math.factorial(blanks)
            else:
                calc = math.pow(choices, blanks)
            res.append((name, calc))
        sorted_names = sorted(res, key=operator.itemgetter(0))
        sorted_values = sorted(sorted_names, key=operator.itemgetter(1))
        return [name for name, value in sorted_values]
        
    def parse_rule(self, rule):
        def cast_type(e):
            try:
                return int(e)
            except ValueError:
                if e == 'F':
                    return False
                return True
        name, rules = rule.split(':')
        return name, [cast_type(r) for r in rules.strip().split()]
        
        
    def binomial_coeff(self, n, k):
        if k < 0 or k > n:
            return 0
        k = min(k, n-k)
        c = 1
        for i in range(k):
            c = c * (n-i) / (i+1)
        return c
    
    def binomial_summation(self, start, n):
        total = 0
        for i in range(start, n+1):
            total += self.binomial_coeff(n, i)
        return total
        


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

def do_test(rules, __expected):
    startTime = time.time()
    instance = Lottery()
    exception = None
    try:
        __result = instance.sortByOdds(rules);
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
    sys.stdout.write("Lottery (550 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("Lottery.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            rules = []
            for i in range(0, int(f.readline())):
                rules.append(f.readline().rstrip())
            rules = tuple(rules)
            f.readline()
            __answer = []
            for i in range(0, int(f.readline())):
                __answer.append(f.readline().rstrip())
            __answer = tuple(__answer)

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(rules, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1425841163
    PT, TT = (T / 60.0, 75.0)
    points = 550 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
