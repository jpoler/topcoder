# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect
import operator

EVEN = False
ODD = True

def even(n):
    return n % 2 == 0

class SettingTents:
    def dist(self, p1, p2):
        # return c^2 to avoid irrationals (guessing not hashable)
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2)**2 + abs(y1 - y2)**2
    
    def cache_distances(self):
        for i in range(-100, 101):
            for j in range(-100, 101):
                dist = i*i+j*j
                try:
                    points = self.points[dist]
                    points.append((i,j))
                except KeyError:
                    self.points[dist] = [(i,j)]

                
    def all_in_grid(self, points, n, m):
        for x,y in points:
            if not (0<=y<=n and 0<=x<=m):
                return False
        return True
    
    def sort_points(self, points):
        first = sorted(points, key=operator.itemgetter(0))
        return sorted(first, key=operator.itemgetter(1))
    
    def check_rhomboid(self, points, n, m):
        if not self.all_in_grid(points, n, m):
            return False, None
        
        d1 = self.dist(points[0], points[1])
        d2 = self.dist(points[0], points[2])
        d3 = self.dist(points[1], points[3])
        d4 = self.dist(points[1], points[3])

        x, y = points[0]
        dims = tuple((xi - x, yi - y) for xi, yi in points)
        res = (d1 == d2 == d3 == d4 and dims not in self.prev_dims)
        return [res, dims]
    
    def between_points(self, point, line):
        ((lx1, ly1), (lx2, ly2)) = line
        px, py = point
        return ((px == lx1 and px == lx2) and (ly1 <= py <= ly2)) or \
            (py == ly1 and py == ly2) and (lx1 <= px <= lx2)
    
    def four_edges(self, points, n, m):
        res = {}
        valid_lines = (
            ((0,0),(0,n)),
            ((0,0),(m,0)),
            ((0,n),(n,m)),
            ((m,0),(n,m)),
        )
        for point in points:
            point_in = False
            for line in valid_lines:
                if self.between_points(point, line):
                    point_in = True
            if not point_in:
                return False
        return True

    def n_rhombs(self, n, m):
        cur_dims = []

        print("inside n_rhombs (n, m):", n, m)
        ans = 0
        furthest = max(n**2, m**2)

        for a in self.a_points:
            ax, ay = a
            for dist in self.points:

                if dist > furthest: # or dist*2 < self.dist(a, (0, m)):
                    continue
                points = self.points[dist]
                for x1, y1 in points:
                    b = (bx, by) = (ax+x1), (ay+y1)
                    for x2, y2 in points:
                        c = (cx, cy) = (ax+x2, ay+y2)
                        if b == c:
                            continue
                        d = (dx, dy) = (bx+x2, by+y2)
                        four_points = [a,b,c,d]
                        res, dims = self.check_rhomboid(four_points, n, m)
                        if res:
                            print(dims)

                            four_points = tuple(self.sort_points(four_points))
                            if self.four_edges(four_points, n, m):
                                if not four_points in self.done:
                                    cur_dims.append(dims)
                                    ans += 1
                                    self.done[four_points] = True

                        # four_points2 = tuple(self.sort_points([a, b, c, d2]))
                        # if d2y == n or d2x == m:
                        #     if not four_points2 in self.done:
                        #         if self.check_rhomboid(four_points2, n, m):
                        #             ans += 1
                        #             self.done[four_points2] = True
        print("done", self.done)
        return ans, cur_dims
                    

    def fitting_rhombs(self, n, m):
        if n > self.N or m > self.M:
            return 0
        return (self.N - n + 1) * (self.M - m + 1)
            
    def add_to_edge(self, x):
        if x == 1:
            return 2
        else:
            return x + 2

    def countSites(self, N, M):
        self.memo = {}
        self.points = {}
        self.done = {}
        self.prev_dims = {}

        print()
        print("N:", N,"M:", M)

        
        self.N, self.M = sorted([N, M], reverse=True)
        self.a_points = [(i, 0) for i in range(self.N+1)] + [(0, i) for i in range(1, self.M+1)]
        self.grid_points = [(i, j) for i in range(self.N+1) for j in range(self.M+1)]
        self.cache_distances()
        n = 1
        m = 1
        n_start = n
        total = 0
        done = False
        while not done:
            if n > self.N:
                if m > self.M:
                    return total
            print("n:", n, "m:", m)
            rhombs, dims1 = self.n_rhombs(n, m)
            fitting = self.fitting_rhombs(n, m)
            print("n-rhombs", rhombs)
            print("fitting-rhombs", fitting)
            total += rhombs*fitting
            if n != m:
                rhombs, dims2 = self.n_rhombs(m, n)
                fitting = self.fitting_rhombs(m, n)
                print("n-rhombs", rhombs)
                print("fitting-rhombs", fitting)
                total += rhombs*fitting
            else:
                dims2 = []
            for dim in itertools.chain(dims1, dims2):
                self.prev_dims[dim] = True

            print("total", total)
            n += 1
            
            if n > self.N:
                n = n_start + 1
                n_start = n
                m += 1
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
