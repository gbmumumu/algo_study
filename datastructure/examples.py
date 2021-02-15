#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from time import time


# 基于有穷观点的能行方法

def gcd(m, n):
    r = m % n
    while r != 0:
        m, n = n, r
        r = m % n

    return n


# 变位词
def find_anagram(wa, wb):
    def solution_1(sa, sb):
        for i in sa:
            if i not in sb:
                return False
        return True

    def solution_2(sa, sb):
        sal = list(sa)
        sbl = list(sb)
        sal.sort()
        sbl.sort()
        if sal != sbl:
            return False
        return True

    def solution_3(sa, sb):
        c1, c2 = [0, ] * 26, [0, ] * 26
        for i, char_a in enumerate(sa):
            pos = ord(char_a) - ord('a')
            c1[pos] = c1[pos] + 1
        for j, char_b in enumerate(sb):
            pos = ord(char_b) - ord('a')
            c2[pos] = c2[pos] + 1

        count = 0
        still_ok = True
        while count < 26 and still_ok:
            if c1[count] != c2[count]:
                still_ok = False
                break
            count += 1

        return still_ok

    for i in range(1, 4):
        t1 = time()
        res = eval('solution_{}(wa, wb)'.format(i))
        t2 = time()
        dt = t2 - t1
        print(res, dt)


# list 方法比较

def test_list():
    def m0():
        l = []
        for i in range(1000):
            l = l + [i]

    def m1():
        l = []
        for i in range(1000):
            l.append(i)

    def m2():
        l = [i for i in range(1000)]

    def m3():  # fastest!
        l = list(range(1000))

    for i in range(4):
        t1 = time()
        eval(f'm{i}()')
        t2 = time()
        print(i, t2 - t1)


if __name__ == "__main__":
    print(gcd(12, 8))
    find_anagram('hello', 'helol')
    test_list()
