# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class Node:
    def __init__(self, key, *edges):
        self.key = key
        self.edges = list(edges)
        self.discovered = False
        self.processed = False
        self.parent = None
        self.cc = None
        self.distance = 0

    def __repr__(self):
        return "<Node (key: {}, edges: {}, discovered {}, processed: {}, parent: {}, distance: {})".format(
            self.key,
            self.edges,
            self.discovered,
            self.processed,
            self.parent,
            self.distance)

        


class Graph:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    def __init__(self, board):
        self.colmax = len(board[0])

        self.rowmax = len(board)
        self.G = {}
        self.board = board
        for i in range(self.rowmax):
            for j in range(self.colmax):
                self.G[(i, j)] = Node((i, j))
                for d in self.directions:
                    p = self.new_point((i, j), d)
                    if self.valid_direction(p):
                        prow, pcol = p
                        if board[prow][pcol] != 'X':
                            self.G[(i, j)].edges.append(p)

        self.connected_components = {}

                        

                    

    def new_point(self, point, direction):
        xrow, ycol = point
        drow, dcol = direction
        nrow, ncol = xrow+ drow, ycol+dcol
        return (nrow, ncol)

    def valid_direction(self, point):
        nrow, ncol = point
        if (0 <= nrow <= self.rowmax - 1) and (0 <= ncol <= self.colmax - 1):
            return True
        return False

    def dfs(self, v, cc):
        nodes = []
        digits = []
        finished = False
        vrow, vcol = v
        nodes.append(v)
        if self.board[vrow][vcol].isdigit():
            digits.append(self.board[vrow][vcol])
        v_node = self.G[(vrow, vcol)]
        v_node.discovered = True
        v_node.cc = cc
        for u in v_node.edges:
            urow, ucol = u
            u_node = self.G[(urow, ucol)]
            if not u_node.discovered:
                u_node.parent = v
                res,resnodes = self.dfs(u, cc)
                digits.extend(res)
                nodes.extend(nodes)
            v_node.processed = True
        return digits, nodes
                
                
                
        
    
    def ccs(self):
        
        cc = -1
        for i in range(self.rowmax):
            for j in range(self.colmax):

                node = self.G[(i, j)]
                if self.board[i][j] == 'X':
                    continue
                if not node.discovered:
                    cc += 1
                    digits, nodes = self.dfs((i,j), cc)
                if not len(digits) in [0, 1]:
                    raise Exception("There should only be one digit per connected component")
                if len(digits) == 1:
                    self.connected_components[cc] = digits[0]
                if len(digits) == 0:
                    self.connected_components[cc] = ""
        
class TouchScreenDialing:
    def getNumber(self, screen, rows, cols):
        g = Graph(screen)
        g.ccs()
        res = ""
        for i in range(len(rows)):
            row, col = rows[i], cols[i]
            if screen[row][col] == 'X':
                continue
            node = g.G[(row, col)]
            if node.cc is not None:
                res += g.connected_components[node.cc]
        return res
                
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

def do_test(screen, rows, cols, __expected):
    startTime = time.time()
    instance = TouchScreenDialing()
    exception = None
    try:
        __result = instance.getNumber(screen, rows, cols);
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
    sys.stdout.write("TouchScreenDialing (1000 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("TouchScreenDialing.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            screen = []
            for i in range(0, int(f.readline())):
                screen.append(f.readline().rstrip())
            screen = tuple(screen)
            rows = []
            for i in range(0, int(f.readline())):
                rows.append(int(f.readline().rstrip()))
            rows = tuple(rows)
            cols = []
            for i in range(0, int(f.readline())):
                cols.append(int(f.readline().rstrip()))
            cols = tuple(cols)
            f.readline()
            __answer = f.readline().rstrip()

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(screen, rows, cols, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1426179750
    PT, TT = (T / 60.0, 75.0)
    points = 1000 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
