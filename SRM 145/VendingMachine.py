# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class VendingMachine:
    def max_index(self, totals):
        max = 0
        max_index = 0
        for i in range(len(totals)):
            if totals[i] > max:
                max = totals[i]
                max_index = i
        return max_index

    def find_shortest_path(self, cur, targ, n):
        l, g = sorted([cur, targ])
        left = abs(g - l)
        right = abs(n - g + l)
        return min(left, right)
    
    def motorUse(self, input_prices, input_purchases):
        def parse_prices(prices):
            ncolumns = prices[0].count(' ') + 1
            columns = [[] for i in range(ncolumns)]
            for shelf in prices:
                s = shelf.strip().split(' ')
                for i in range(len(s)):
                    columns[i].append(int(s[i]))

            return columns

        def parse_purchases(purchases):
            return_purchases = []
            for purch in purchases:
                indices, time = purch.strip().split(':')
                time = int(time)
                shelf, column = [int(index) for index in indices.split(',')]
                return_purchases.append((time, column, shelf))
            return return_purchases

        prices = parse_prices(input_prices)
        purchases = parse_purchases(input_purchases)

        column_totals = [sum(column) for column in prices]
        columns = len(column_totals)
        current_index = 0
        distance = 0
        last_time = 0
        time = 0
        start = True
        finish = False
        for i in range(0, len(purchases)+ 1):
            if i == len(purchases):
                finish = True
            else:
                time, column, shelf = purchases[i]
            if time - last_time >= 5 or start or finish:
                start = False
                target = self.max_index(column_totals)
                distance += self.find_shortest_path(current_index, target, columns)
                current_index = target
                if finish:
                    break

            last_time = time
            price = prices[column][shelf]
            if prices[column][shelf] == False:
                return -1
            prices[column][shelf] = False
            column_totals[column] -= price
            distance += self.find_shortest_path(current_index, column, columns)
            current_index = column
            
        return distance

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

def do_test(prices, purchases, __expected):
    startTime = time.time()
    instance = VendingMachine()
    exception = None
    try:
        __result = instance.motorUse(prices, purchases);
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
    sys.stdout.write("VendingMachine (1100 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("VendingMachine.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            prices = []
            for i in range(0, int(f.readline())):
                prices.append(f.readline().rstrip())
            prices = tuple(prices)
            purchases = []
            for i in range(0, int(f.readline())):
                purchases.append(f.readline().rstrip())
            purchases = tuple(purchases)
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(prices, purchases, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1426015486
    PT, TT = (T / 60.0, 75.0)
    points = 1100 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
