# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect
from itertools import zip_longest

class PlayingCubes:
    def find_cube_matching(self, word):
        # maximum bipartite matching until either 1) can't match up to 
        # len(word) or 2) find a matching with |A| == len(matching)
        A = [[i for i in range(len(self.cubes)) if c in self.cubes[i]]
             for c in word]
        
        A_match = [None for _ in range(len(A))]
        B_match = [None for _ in range(len(self.cubes))]
        match_cardinality = 0
        for source in range(len(A)):
            if match_cardinality >= len(word):
                break

            # bfs to find augmenting paths
            found_path = False
            parents = [None for _ in range(len(A))]
            parents[source] = source
            q = collections.deque()
            q.append(source)
            while (q and not found_path):
                where = q.popleft()
                for i in range(len(A[where])):
                    match = A[where][i]
                    nxt = B_match[match]
                    if where != nxt:
                        if nxt == None:
                            found_path = True
                            break
                        if parents[nxt] is None:
                            q.append(nxt)
                            parents[nxt] = where
            if not found_path:
                continue
            while parents[where] != where:
                temp_match = A_match[where]
                A_match[where] = match
                B_match[match] = where
                where = parents[where]
                match = temp_match
            A_match[where] = match
            B_match[match] = where
            match_cardinality += 1

        return match_cardinality >= len(word)
                    
                                
                        
                    
                
            
            
        
                   
    
    
    def composeWords(self, cubes, words):
        ans = []
        self.cubes = [dict(zip_longest(cube, [], fillvalue=True))
                      for cube in cubes]
        for i in range(len(words)):
            if self.find_cube_matching(words[i]):
                ans.append(i)
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

def do_test(cubes, words, __expected):
    startTime = time.time()
    instance = PlayingCubes()
    exception = None
    try:
        __result = instance.composeWords(cubes, words);
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
    sys.stdout.write("PlayingCubes (250 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("PlayingCubes.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            cubes = []
            for i in range(0, int(f.readline())):
                cubes.append(f.readline().rstrip())
            cubes = tuple(cubes)
            words = []
            for i in range(0, int(f.readline())):
                words.append(f.readline().rstrip())
            words = tuple(words)
            f.readline()
            __answer = []
            for i in range(0, int(f.readline())):
                __answer.append(int(f.readline().rstrip()))
            __answer = tuple(__answer)

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(cubes, words, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1426457902
    PT, TT = (T / 60.0, 75.0)
    points = 250 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
