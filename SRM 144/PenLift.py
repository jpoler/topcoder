# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect,operator
import pdb

class Point:
    def __init__(self, *coords):
        self.point = tuple(coords)
        self.x, self.y = coords
        self.discovered = self.processed = False
        self.parent = None
        self.edges = []

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

    def __le__(self, other):
        if self.x == other.x:
            return self.y <= other.y
        else:
            return self.x <= other.x
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    
    def __gt__(self, other):
        if self.x == other.x:
            return self.y > other.y
        else:
            return self.x > other.x

    def __ge__(self, other):
        if self.x == other.x:
            return self.y >= other.y
        else:
            return self.x >= other.x
        
    def __repr__(self):
        return "<Point ({}, {}) edges: {}>".format(self.x, self.y, self.edges)

class Segment:
    def __init__(self, *points):
        self.less, self.more = sorted(points)
        
    def is_horiz(self):
        return self.less.y == self.more.y

    def is_vert(self):
        return self.less.x == self.more.x

    def perp_intersection(self, p):
        if self.is_horiz():
            return p.y == self.less.y and p.y == self.more.y and \
                (self.less.x < p.x < self.more.x)
        else:
            return p.x == self.less.x and p.x == self.more.x and \
                (self.less.y < p.y < self.more.y)
        

    def overlaps(self, other):
        return self.less < other.less < self.more < other.more or \
            other.less < self.less < other.more < self.more

    def __repr__(self):
        return "<Segment (less: {}, more: {})>".format(self.less, self.more)

class PenLift:
    def parse_seg(self, segment):
        return list(map(int, segment.strip().split(' ')))

    def merge_segs(self, seg1, seg2):
        if seg1.less < seg2.less:
            return Segment(seg1.less, seg2.more)
        elif seg2.less < seg1.less:
            return Segment(seg2.less, seg1.more)
        assert True == False

    def split_segment(self, p, seg):
        if not seg.perp_intersection(p):
            raise ValueError("Trying to split a line segment " \
                             "that doesn't intersect the given " \
                             "point: point: {}, segment: {}".format(p, seg))
        # print("in split_segment", p, seg)
        return Segment(seg.less, p), Segment(p, seg.more)
    
    def merge_segment_list(self, segments):
        merged_segs = []
        merges = 0
        new_segs = []
        sorted_segs = sorted(segments, key=operator.attrgetter('less'))
        start = sorted_segs[0]
        start_index = 0
        for i in range(0, len(segments)):
            less, more = sorted_segs[i-1], sorted_segs[i]
            if less.overlaps(more):
                continue
            if start_index < i - 1:
                new_seg = self.merge_segs(sorted_segs[start_index], less)
                merged_segs.append(new_seg)
                new_segs.append(new_seg)
                
            else:
                new_segs.append(less)
            start = more
            start_index = i
        return new_segs
                
    def append_segment(self, dct, seg, axis):
        coord = getattr(seg.less, axis)
        try:
            dct[coord].append(seg)
        except KeyError:
            dct[coord] = [seg]

    # I am aware that this could end up being O(n^2) worst-case
    # if it sucks I'll use an interval tree for O(nlgn)

    # sidenote: it already does suck but I don't want to write an interval tree
    # due to time constraints
    def split_intersections(self, src_segs, trg_segs):
        
        for coord, segs in src_segs.items():
            if isinstance(segs, str):
                continue
            for seg in segs:

                for point in [seg.less, seg.more]:
                    try:
                        trg_segs_lst = trg_segs[getattr(point, trg_segs['coord_axis'])]
                    except KeyError:
                        continue
                    new_lst = []
                    for perp in trg_segs_lst:
                        if perp.perp_intersection(point):
                            # print("original", perp)
                            # print("point", point)
                            new_segs = self.split_segment(point, perp)
                            # print("new", new_segs)
                            new_lst.extend(new_segs)
                        else:
                            new_lst.append(perp)
                    trg_segs[getattr(point, trg_segs['coord_axis'])] = new_lst
        return src_segs, trg_segs


                        
                

    def merged_segs(self, segments):
        vert_segs = {}
        horiz_segs = {}
        merged_vert_segs = {'coord_axis': 'x'}
        merged_horiz_segs = {'coord_axis': 'y'}


        for segment in segments:
            s = self.parse_seg(segment)
            seg = Segment(Point(*s[:2]), Point(*s[2:]))
            if seg.is_horiz():
                self.append_segment(horiz_segs, seg, 'y')
            else:
                self.append_segment(vert_segs, seg, 'x')

        for coord, segs in horiz_segs.items():
            merged_horiz_segs[coord] = self.merge_segment_list(segs)
        for coord, segs in vert_segs.items():
            merged_vert_segs[coord] = self.merge_segment_list(segs)


        merged_horiz_segs, split_vert_segs = self.split_intersections(
            merged_horiz_segs,
            merged_vert_segs,
        )
        split_vert_segs, split_horiz_segs = self.split_intersections(
            split_vert_segs,
            merged_horiz_segs,
        )
        return_segs = []
        
        # print(split_horiz_segs)
        # print(split_vert_segs)
        for coord, segs in split_horiz_segs.items():
            if isinstance(coord, str):
                continue
            return_segs.extend(segs)
        for coord, segs, in split_vert_segs.items():
            if isinstance(coord, str):
                continue
            return_segs.extend(segs)    
        
        return return_segs

    def merge_dct_lists(self, *dcts):
        return_list = []
        for dct in dcts:
            for lst in dct.values():
                return_list.extend(lst)
        return return_list

    def score_connected_components(self, cc):
        paths = 0
        for cc, odds in cc.items():
            paths += max(1, odds/2)
        return paths - 1
    
    def numTimes(self, segments, n):
        # pdb.set_trace()
        print(segments)
        edges  = self.merged_segs(segments)
        print(edges)


        g = Graph(n, *edges)

        g.connected_components()
        print("g.G", g.G)
        print("cc", g.cc)

        return self.score_connected_components(g.cc)
        
        

class Graph:
    def __init__(self, traversals, *segments):

        self.G = {}
        for seg in segments:

            self.insert_segement(seg)
        self.cc = {}
        self.traversals = traversals

    def insert_segement(self, seg):
        try:
            self.G[seg.less.point].edges.append(seg.more.point)
        except KeyError:
            self.G[seg.less.point] = seg.less
            seg.less.edges.append(seg.more.point)
        try:
            self.G[seg.more.point].edges.append(seg.less.point)
        except KeyError:
            self.G[seg.more.point] = seg.more
            seg.more.edges.append(seg.less.point)

    def bfs(self, start):
        q = collections.deque()
        q.append(start)
        start_node = self.G[start]
        start_node.discovered = True
        while q:
            u = q.popleft()
            u_node = self.G[u]
            self.process_vertex_early(u)
            for v in u_node.edges:
                v_node = self.G[v]
                self.process_edge(u, v)
                if not v_node.discovered:
                    v_node.discovered = True
                    v_node.parent = u
                    q.append(v)
            self.process_vertex_late(u)
            u_node.processed = True

    def process_vertex_early(self, v):
        v_node = self.G[v]
        if self.current_cc not in self.cc:
            self.cc[self.current_cc] = 0
        if len(v_node.edges)*self.traversals % 2 == 1:
            self.cc[self.current_cc] = self.cc.get(self.current_cc, 0) + 1
            
    def process_edge(self, u, v):
        pass

    def process_vertex_late(self, v):
        pass
        
    def connected_components(self):
        pdb.set_trace()
        self.current_cc = -1
        
        for v in self.G.keys():
            if not self.G[v].discovered:
                self.current_cc += 1
                self.bfs(v)
    
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

def do_test(segments, n, __expected):
    startTime = time.time()
    instance = PenLift()
    exception = None
    try:
        __result = instance.numTimes(segments, n);
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
    sys.stdout.write("PenLift (1100 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("PenLift.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            segments = []
            for i in range(0, int(f.readline())):
                segments.append(f.readline().rstrip())
            segments = tuple(segments)
            n = int(f.readline().rstrip())
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(segments, n, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1425866234
    PT, TT = (T / 60.0, 75.0)
    points = 1100 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
