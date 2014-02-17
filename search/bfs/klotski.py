#!/usr/bin/python

# klotski.py
# Copyright (C) 2014 Liu Xinyu (liuxinyu95@gmail.com)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# `Heng Dao Li Ma' layout
# 1 A A 2
# 1 A A 3
# 3 4 4 5
# 3 7 8 5
# 6 0 0 9

START = [[(1, 1), (2, 1)],
         [(1, 4), (2, 4)],
         [(3, 1), (4, 1)],
         [(3, 2), (3, 3)],
         [(3, 4), (4, 4)],
         [(5, 1)], [(4, 2)], [(4, 3)], [(5, 4)],
         [(1, 2), (1, 3), (2, 2), (2, 3)]]

def solve(start):
    visit = [normalize(start)]
    queue = [(start, [])]
    while queue != []:
        (cur, seq) = queue.pop(0)
        print "try", len(seq), "steps"
        if cur[-1] == [(4, 2), (4, 3), (5, 2), (5, 3)]:
            return seq[::-1] # reversed(seq)
        else:
            for delta in expand(cur, visit):
                brd = move(cur, delta)
                queue.append((brd, [delta]+seq))
                visit.append(normalize(brd))
    return [] # no solution

def expand(layout, visit):
    def bound(y, x):
        return 1 <= y and y <= 5 and 1 <= x and x <= 4
    def valid(m, i, y, x):
        return m[y - 1][x - 1] in [0, i]
    def unique(i, dy, dx):
        b = move(layout, (i, (dy, dx)))
        return normalize(b) not in visit and normalize(mirror(b)) not in visit
    s = []
    d = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    m = matrix(layout)
    for i in range(1, 11):
        for (dy, dx) in d:
            if all([bound(y + dy, x + dx) and valid(m, i, y + dy, x + dx)
                    for (y, x) in layout[i - 1]]) and unique(i, dy, dx):
                s.append((i, (dy, dx)))
    return s

def dup(layout):
    return [r[:] for r in layout]

def matrix(layout):
    m = [[0]*4 for _ in range(5)]
    for (i, ps) in zip(range(1, 11), layout):
        for (y, x) in ps:
            m[y - 1][x - 1] = i
    return m

def move(layout, delta):
    (i, (dy, dx)) = delta
    m = dup(layout)
    m[i - 1] = [(y + dy, x + dx) for (y, x) in m[i - 1]]
    return m

def mirror(layout):
    return [[(y, 5 - x) for (y, x) in r] for r in layout]

def normalize(layout):
    return sorted([sorted(r) for r in layout])

# pretty print
def output(layout, seq):
    def prt(m):
        for r in m:
            print ["%X" % x for x in r]
        print "\n",
    prt(matrix(layout))
    for (i, (dy, dx)) in seq:
        layout[i - 1] = [(y + dy, x + dx) for (y, x) in layout[i - 1]]
        prt(matrix(layout))
    print "total", len(seq), "steps"

if __name__ == "__main__":
    output(START, solve(START))